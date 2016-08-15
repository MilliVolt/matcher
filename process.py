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
                file_list.extend(os.path.join(root, f));
    return file_list

music_list = get_file_list(MUSIC_DIR)
video_list = get_file_list(VIDEO_DIR)

for m in music_list:
    best_match = {'score':0}
    for v in video_list:
        with open(m) as music, open(v) as video:
            score = matcher.compatibility(
                        list(map(float, video.readlines())),
                        list(map(float, music.readlines()))
                    )
        if (score.score > best_match['score']):
            best_match = {'video' : v,
                          'music' : m,
                          'score' : score.score,
                          'offset': score.offset,
                          'delay' : score.delay}
    print(best_match)

        





