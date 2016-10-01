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

import numpy as np
from numpy.fft import fft, ifft, fft2, ifft2, fftshift
from scipy import signal
 
def cross_correlation_using_fft(x, y):
    f1 = fft(x)
    f2 = fft(np.flipud(y))
    cc = np.real(ifft(f1 * f2))
    return fftshift(cc)

def cc_from_file(file1, file2):
    f1 = np.loadtxt(file1)
    f2 = np.loadtxt(file2)
    import ipdb; ipdb.set_trace()
    return match(f1, f2)

def rfft_xcorr(x, y):
    M = len(x) + len(y) - 1
    N = 2 ** int(np.ceil(np.log2(M)))
    X = np.fft.rfft(x, N)
    Y = np.fft.rfft(y, N)
    cxy = np.fft.irfft(X * np.conj(Y))
    cxy = np.hstack((cxy[:len(x)], cxy[N-len(y)+1:]))
    return cxy

def ffi_match(x, ref):
    cxy = rfft_xcorr(x, ref)
    index = np.argmax(cxy)
    if index < len(x):
        return index
    else: # negative lag
        return index - len(cxy)

Match = namedtuple(
    'Match',
    'scaled_score, score, offset, delay, master_seek, candidate_seek'
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
    return np.count_nonzero(np.abs(aux[1:] - aux[:-1]) < threshold)


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


def compatibility(master, candidate, threshold=None):
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
    master = np.array(master)
    candidate = np.array(candidate)
    size = master.size

    # instead of iteerate through all possible offsets, we use ffi to figure
    # out the correct offset
    offset = ffi_match(master, candidate)

    # The sample is a "window" into the candidate the same size as the
    # master that slides from left to right
    sample = candidate[max(offset, 0) : size + offset]

    # The offset into the master array goes from right to left, stopping
    # at the first element of the master
    master_offset = -min(offset, 0)

    # Since we are interested in the spacing between values, we add a delay
    # to the sample so that its first value matches the master exactly
    delay = master[master_offset] - sample[0]
    delayed_sample = sample + delay

    # The compatibility score is the number of close matches between the
    # sample and the section of the master array it covers
    score = count_fuzzy_set_intersection(master, delayed_sample, threshold)

    # Scale it by the size of the master array
    scaled = score / size

    # Determine the seek values for the master and candidate. The
    # difference between these values is the delay between the tracks.
    mast_seek, cand_seek = get_seek_values(master, master_offset, delay)

    # We want the earliest part of the master array that maximizes
    # compatibility, so any score greater than or equal to the highest
    # score we've seen becomes the highest score
    match = Match(scaled, score, offset, delay, mast_seek, cand_seek)

    return match


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
