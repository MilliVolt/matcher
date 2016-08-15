#!/usr/bin/env python3
"""Match master stream to candidate stream

Example usage:
    master = master_audio_track()
    candidate = candidate_audio_track()
    match = compatibility(master, candidate)
    print('compatibility score: {}'.format(match.score))
    print('array offset: {}'.format(match.offset))
    print('track delay: {}'.format(match.delay))
"""
import argparse
from collections import namedtuple

import numpy as np


Match = namedtuple('Match', 'score, offset, delay')


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
    aux.sort()
    return np.count_nonzero(np.abs(aux[1:] - aux[:-1]) < threshold)


def compatibility(master, candidate, threshold=0.022):
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
        score: The number of coincidental values between the master and the
            candidate.
        offset: The steps to move the candidate array in order to maximize
            compatibility with the master array.
        delay: The difference between the value of the master array and the
            value of the candidate array at the offset. When "playing" the
            candidate versus the master, this (combined with the offset) tells
            you when to start playing.
    """
    master = np.array(master)
    candidate = np.array(candidate)
    size = master.size
    best_match = Match(0, 0, 0)

    # "Slide" the candidate array across the master array
    for offset in range(-size + 1, len(candidate)):
        # The sample is a "window" into the candidate the same size as the
        # master that slides from left to right
        sample = candidate[max(offset, 0) : size + offset]

        # The offset into the master array goes from right to left, stopping
        # at the first element of the master
        master_offset = -(size + min(offset, 0))

        # Since we are interested in the spacing between values, we add a delay
        # to the sample so that its first value matches the master exactly
        delay = master[master_offset] - sample[0]
        delayed_sample = sample + delay

        # The compatibility score is the number of close matches between the
        # sample and the section of the master array it covers
        score = count_fuzzy_set_intersection(master, delayed_sample, threshold)

        # We want the earliest part of the master array that maximizes
        # compatibility, so any score greater than or equal to the highest
        # score we've seen becomes the highest score
        match = Match(score, offset, delay)
        if match.score >= best_match.score:
            best_match = match

    return best_match


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('track1', type=argparse.FileType())
    parser.add_argument('track2', type=argparse.FileType())
    args = parser.parse_args()
    with args.track1 as track1:
        track_1 = list(map(float, track1.readlines()))
    with args.track2 as track2:
        track_2 = list(map(float, track2.readlines()))
    match = compatibility(track_1, track_2)
    print('{m.score},{m.offset},{m.delay}'.format(m=match))


if __name__ == '__main__':
    main()
