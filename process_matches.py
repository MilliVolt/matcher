#!/usr/bin/env python3
"""Add matches to the database."""
import asyncio
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from multiprocessing import cpu_count

from sqlalchemy.orm import sessionmaker

import models
from matcher import compatibility


engine = models.create_engine()
session = sessionmaker(bind=engine, autocommit=True)()
cpus = cpu_count()
queue = asyncio.Queue(cpus)


def record_match(unmatch):
    """Make a TrackMatch.

    Given a row from models.get_unmatched, create a TrackMatch.
    """
    engine.dispose()
    get = session.query(models.Video).get
    track = get(str(unmatch.track_id))
    match = get(str(unmatch.match_id))
    if unmatch.master_type == 'video':
        master = track.video_shot_times
        candidate = match.audio_beat_times
    else:
        master = track.audio_beat_times
        candidate = match.video_shot_times
    compat = compatibility(master, candidate)
    with session.begin():
        session.add(models.TrackMatch(
            track=track,
            match=match,
            master_type=unmatch.master_type,
            score=compat.score,
            scaled_score=compat.scaled_score,
            track_seek=compat.master_seek,
            match_seek=compat.candidate_seek,
        ))


async def make_matches(loop):
    """Process unmatched videos and wait a minute if there are none."""
    spawn = partial(loop.run_in_executor, None, record_match)
    while True:
        unmatched = models.get_unmatched(session)
        if not unmatched.rowcount:
            await asyncio.sleep(60)
            continue
        await asyncio.wait([spawn(unmatch) for unmatch in unmatched])


async def produce_tasks():
    while True:
        await queue.put(get_task_parameters())


async def consume_tasks():
    while True:
        task_params = await queue.get()
        proc = await asyncio.create_subprocess_exec(process_name, task_params,
            stdout=asyncio.subprocess.PIPE)
        data = await proc.stdout.readline()
        line = data.decode().rstrip()
        await proc.wait()
        do_something_with(line)


def main():
    """Use a process pool to carry out tasks."""
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        loop.set_default_executor(executor)
        asyncio.ensure_future(make_matches(loop))
        asyncio.ensure_future(produce_tasks())
        for _ in range(cpus):
             asyncio.ensure_future(consume_tasks())
        loop.run_forever()
        loop.close()


if __name__ == '__main__':
    main()
