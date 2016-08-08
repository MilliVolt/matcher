#!/usr/bin/env python3

from collections import namedtuple

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist


Match = namedtuple('Match', 'offset, candidate_index')


def match(master, candidates):
    """Find the most compatible candidate

    http://stackoverflow.com/a/38798544/1475412
    """
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
    distances = cdist(padded_candidates, sliding_master)

    # The most compatible candidate has the shortest euclidean distance
    # to the master
    return Match(distances.min(0).argmin(), distances.min(1).argmin())
