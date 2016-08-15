import matcher
import os
import re

MUSIC_DIR = '../music'
VIDEO_DIR = '../video'

def get_file_list(d):
    file_list = []
    # getting all the files in d
    for root, dirs, files in os.walk(d):
        for f in files:
            if re.search(r'\.txt$', f):
                file_list.append(os.path.join(root, f));
    return file_list

music_list = get_file_list(MUSIC_DIR)
video_list = get_file_list(VIDEO_DIR)

for v in video_list:
    best_match = {'score':0}
    for m in music_list:
        with open(m) as music, open(v) as video:
            vl = list(map(float, video.readlines()))
            ml = list(map(float, music.readlines()))
        if vl and ml:
            score = matcher.compatibility(vl, ml)
            if (score.score > best_match['score']):
                best_match = {'video' : v,
                              'music' : m,
                              'score' : score.score,
                              'offset': score.offset,
                              'delay' : score.delay}
    print(best_match)

        





