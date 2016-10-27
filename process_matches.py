#!/usr/bin/env python3
"""Add matches to the database."""
import asyncio
from concurrent.futures import ProcessPoolExecutor
from functools import partial
import time

from sqlalchemy.orm import sessionmaker

import models
from matcher import compatibility


engine = models.create_engine()
session = sessionmaker(bind=engine, autocommit=True)()


def record_match(unmatch):
    """Make a TrackMatch.

    Given a row from models.get_unmatched, create a TrackMatch.
    """
    engine.dispose()
    get = session.query(models.Video).get
    from_audio = get(str(unmatch.from_id))
    to = get(str(unmatch.to_id))
    compat = compatibility(from_audio.audio_beat_times, to.audio_beat_times)
    with session.begin():
        session.add(models.AudioSwap(
            from_audio=from_audio,
            to_audio=to,
            score=compat[0] or 1,
            scaled_score=compat[1],
            from_seek=compat[3],
            to_seek=compat[4],
        ))


async def make_matches(loop):
    """Process unmatched videos and wait a minute if there are none."""
    spawn = partial(loop.run_in_executor, None, record_match)
    prev = time.time()
    while True:
        unmatched = models.get_unmatched(session)
        if not unmatched.rowcount:
            print('sleeping for 60 seconds')
            await asyncio.sleep(60)
            continue
        print('processing {} unmatches...'.format(unmatched.rowcount), end='')
        await asyncio.wait([spawn(unmatch) for unmatch in unmatched])
        new_time = time.time()
        print(' {:.3f} seconds, {:.6f} seconds/match'.format(
            new_time - prev, (new_time - prev)/unmatched.rowcount))
        prev = new_time


def main():
    """Use a process pool to carry out tasks."""
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        loop.set_default_executor(executor)
        asyncio.ensure_future(make_matches(loop))
        loop.run_forever()
        loop.close()


if __name__ == '__main__':
    main()
