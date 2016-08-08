#!/usr/bin/env python3
"""Match master stream to candidate streams

Example usage
-------------
master = master_audio_track()
candidates = list(candidate_audio_tracks())

dist = candidate_distance_matrix(master, candidates)
rankings = sorted_candidates(dist)
best_candidate = rankings[0]
offset = candidate_offset(dist, best_candidate)

print('The best candidate is {} with offset {}'.format(best_candidate, offset))
-------------

http://stackoverflow.com/a/38798544/1475412
"""

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist


def candidate_distance_matrix(master, candidates):
    """Compute the distance matrix between the master and candidates."""
    # Get master and candidates into useful objects
    np_master = np.array(master)
    padded_candidates = pd.DataFrame(candidates).fillna(0)

    # If the master length is too short, tile it
    candidate_length = padded_candidates.shape[1]

    if np_master.size < candidate_length:
        tiles = candidate_length // np_master.size + 1
        np_master = np.tile(np_master, tiles)

    master_length = np_master.size

    # Broadcast to get sliding window matrix
    master_window = np.arange(master_length - candidate_length + 1)[:, None]
    candidate_window = np.arange(candidate_length)
    sliding_master = np_master[master_window + candidate_window]

    # Compute distances between each sliding window and the candidates
    return cdist(padded_candidates, sliding_master)


def sorted_candidates(distance_matrix):
    """Return the candidate indices sorted by compatibility with the master."""
    return distance_matrix.min(1).argsort()


def candidate_offset(distance_matrix, candidate_index):
    """Return the offset that maximizes candidate compatibility with master."""
    return distance_matrix[candidate_index].argmin()
