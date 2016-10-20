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


Match = namedtuple(
    'Match',
    'scaled_score, score, delay, master_seek, candidate_seek'
)


@numba.njit()
def get_score(master, sample, delay, threshold, offset=None):
    i = j = 0
    score = 0
    s = sample[j] + delay
    sample_end = sample.size - 1
    while i < master.size:
        while j < sample_end and s < master[i] - threshold:
            j += 1
            s = sample[j] + delay
        if np.abs(s - master[i]) <= threshold:
            score += 1
        i += 1
    return score


@numba.njit()
def best_match(master, candidate, threshold):
    best_score = 0
    rest = (0, 0, 0, 0)
    for offset in range(1 - master.size, candidate.size):
        sample = candidate[max(offset, 0) : master.size + offset]
        master_offset = -min(offset, 0)
        delay = master[master_offset] - sample[0]
        score = get_score(master, sample, delay, threshold, offset=offset)
        if score >= best_score:
            best_score = score
            mast_seek = master[master_offset - 1] if master_offset else 0
            cand_seek = mast_seek - delay
            if cand_seek < 0:
                mast_seek = master[master_offset]
                cand_seek = mast_seek - delay
            rest = (score / master.size, delay, mast_seek, cand_seek)
    return (rest[0], best_score, rest[1], rest[2], rest[3])


def compatibility(master, candidate, threshold=None):
    if threshold is None:
        threshold = 0.022
    master = np.array(master, dtype=np.float64)
    candidate = np.array(candidate, dtype=np.float64)
    return best_match(master, candidate, threshold)

def compatibility_from_files(file_name_1, file_name_2, threshold=None):
    """Return the compatibility for the values in the two given files."""
    fn1, fn2 = file_name_1, file_name_2
    #return compatibility(np.loadtxt(fn1), np.loadtxt(fn2), threshold)
    a = np.arange(10000)
    return compatibility(a, a, threshold)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('track1')
    parser.add_argument('track2')
    args = parser.parse_args()
    match = compatibility_from_files(args.track1, args.track2)
    print(Match(*match)._asdict())


if __name__ == '__main__':
    main()
