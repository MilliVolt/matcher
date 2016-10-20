#!/usr/bin/env python3
"""Match master stream to candidate stream

Example usage:
    master = master_audio_track()
    candidate = candidate_audio_track()
    match = compatibility(master, candidate)
    print('scaled compatibility score: {}'.format(match.scaled_score))
    print('compatibility score: {}'.format(match.score))
    print('array offset: {}'.format(match.offset))
    print('track delay: {}'.format(match.delay))
    print('master delay: {}'.format(match.master_seek))
    print('candidate delay: {}'.format(match.candidate_seek))
"""
import argparse
from collections import namedtuple

import numba

import numpy as np

from scipy.signal import fftconvolve


Match = namedtuple(
    'Match',
    'scaled_score, score, delay, master_seek, candidate_seek'
)


def count_fuzzy_set_intersection(ar1, ar2, threshold):
    """Find the size of the fuzzy intersection of two arrays.

    Return the number of values that have a close match (the absolute
    difference is less than the given threshold). Compare to set intersection,
    where the match has to be exact.

    This will give an erroneous result if either array contains values that are
    within the threshold of each other.

    Based on:
    github.com/numpy/numpy/blob/v1.11.1/numpy/lib/arraysetops.py#L218-L259
    """
    aux = np.concatenate((ar1, ar2))
    aux.sort(kind='mergesort')
    return np.count_nonzero(aux[1:] - aux[:-1] < threshold)


def get_seek_values(master, master_offset, delay):
    """Get the seek values for the master and candidate.

    This attempts to seek to the value immediately before the master_offset
    (which represents the first "matching" value between the master and
    candidate) for the master seek, then apply the delay to get the candidate
    seek, so that "playing" the two tracks with the given seek values has the
    tracks sync up.

    For example, if these represent times in seconds:

    [1 3 7 8 9]  # master
    [    5 6 7]  # candidate

    would give a master seek of 3 and a candidate seek of 1, so that the first
    "match" occurs in each track at 4 seconds.

    However, in this scenario:

    [1 3 7 8 9]  # master
    [    2 3 4]  # candidate

    the master seek should be 3 and the candidate seek should be -2. We can't
    have a negative seek, so we just use the first "sync" location: the master
    seek is 7 and the candidate seek is 2.
    """
    master_seek = master[master_offset - 1] if master_offset else 0
    candidate_seek = master_seek - delay
    if candidate_seek < 0:
        master_seek = master[master_offset]
        candidate_seek = master_seek - delay
    return master_seek, candidate_seek


@numba.njit()
def fuzzy_mode_idx(arr, threshold):
    result = (0, 0)
    longest = 0
    i = j = 0
    end = len(arr)
    while i < end:
        if j < end and arr[j] - arr[i] <= threshold:
            current_distance = j - i
            if current_distance > longest:
                longest = current_distance
                result = (i, j)
            j += 1
        else:
            i += 1
    return result


def compatibility(master, candidate, threshold=None):
    if threshold is None:
        threshold = 0.022

    master = np.array(master, dtype=np.float32)
    candidate = np.array(candidate, dtype=np.float32)
    diff = master - candidate[:, np.newaxis]
    delays = np.ravel(diff).copy()
    delays.sort(kind='mergesort')
    left, right = fuzzy_mode_idx(delays, threshold)
    score = right - left + 1
    scaled = score / master.size
    small = delays[left]
    big = delays[right]
    hits = np.where(np.logical_and(small <= diff, diff <= big))
    master_offset = hits[1][0]
    cand_offset = hits[0][0]
    delay = diff[cand_offset, master_offset]
    mast_seek, cand_seek = get_seek_values(master, master_offset, delay)
    return Match(scaled, score, delay, mast_seek, cand_seek)


def compatibility2(master, candidate, threshold=None):
    """Determine the compatibility of the candidate to the master.

    The master and the candidate should be arrays of monotonically increasing
    positive values, each with spacing between the values of at least the
    threshold value.

    In this case compatibility means the number of close matches with respect
    to the spacing of the values. If master is an array of shot times for a
    video and candidate is an array of beat times in an audio track,
    compatibility is high if the two arrays "match up".

    The default threshold comes from the strictest value here:
    en.wikipedia.org/w/index.php?title=Audio_to_video_synchronization
    &oldid=728675183#Recommendations

    This function returns a Match object with the following attributes:
        scaled_score: The score divided by the length of the master.
        score: The number of coincidental values between the master and the
            candidate.
        offset: The steps to move the candidate array in order to maximize
            compatibility with the master array. Not needed for syncing.
        delay: The difference between the value of the master array and the
            value of the candidate array at the offset. If this value is
            negative, seek by the value of -delay into the candidate track. If
            this value is 0, play both tracks at the same time with no seeking.
            If this value is positive, seek by the value of delay into the
            master track.
    """
    if threshold is None:
        threshold = 0.022

    # The sample frequency is just high enough to distinguish the treshold
    frequency = int(np.ceil(1 / threshold))
    master = np.array(master)
    candidate = np.array(candidate)

    # The total number of samples is the higher duration times the frequency
    # times 2 (to make fft happy) plus one??? seems to fix some boundary
    # problems
    duration = int(np.ceil(float(max(master[-1], candidate[-1]))))
    num_samples = duration * frequency + 1

    # sm and sc are the square-wave versions of the master and candidate:
    # 1 where a sample has a beat, 0 otherwise
    sm = np.zeros(num_samples)
    master_hits = np.round(
        np.fromiter(map(float, master * frequency), dtype=float)).astype(int)
    sm[master_hits] = 1
    sc = np.zeros(num_samples)
    candidate_hits = np.round(
        np.fromiter(map(float, candidate * frequency), dtype=float)).astype(int)
    sc[candidate_hits] = 1

    # xcor is the cross-correlation calculated using fft
    xcor = fftconvolve(sm, sc[::-1])

    # shift is the phase shift between sm and sc, or the delay measured in
    # number of samples
    shift = xcor.argmax() + 1 - num_samples
    if shift > num_samples:
        shift -= num_samples - 1

    # the offsets are the indices of the first coincidental beat between the
    # master and the shifted candidate
    master_offset = np.roll(sc, shift)[sm == 1].argmax()
    candidate_offset = np.searchsorted(
        candidate_hits + shift, master_hits[master_offset])

    # the delay is the difference in seconds between the timestamps of the
    # first coincidental beat
    delay = master[master_offset] - candidate[candidate_offset]

    # since (potentially) only part of the candidate covers the master, we only
    # look at the part of it that is covered
    delayed = candidate + delay
    candidate_sample = delayed[master_offset : master.size + master_offset]
    score = count_fuzzy_set_intersection(master, candidate_sample, threshold)
    scaled = score / master.size
    mast_seek, cand_seek = get_seek_values(master, master_offset, delay)
    return Match(scaled, score, delay, mast_seek, cand_seek)


def compatibility_from_files(file_name_1, file_name_2, threshold=None):
    """Return the compatibility for the values in the two given files."""
    fn1, fn2 = file_name_1, file_name_2
    return compatibility(np.loadtxt(fn1), np.loadtxt(fn2), threshold)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('track1')
    parser.add_argument('track2')
    args = parser.parse_args()
    match = compatibility_from_files(args.track1, args.track2)
    print(match._asdict())


if __name__ == '__main__':
    main()
