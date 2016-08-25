"""Postgres

To add tracks:
    with session.begin():
        session.add(Video(url_id=<url_id>, duration=<duration>)

To add matches:
    track_query = session.query(Video).filter_by(url_id=<url_id_0>)
    match_1_query = session.query(Video).filter_by(url_id=<url_id_1>)
    match_2_query = session.query(Video).filter_by(url_id=<url_id_2>)
    with session.begin():
        session.add(TrackMatch(
            track=track_query.one(), match=match_1_query.one(),
            master_type=<'video' or 'audio'>,
            score=<score>, scaled_score=<scaled_score>,
            track_seek=<track_seek>, match_seek=<match_seek>,
        ))
        session.add(TrackMatch(
            track=track_query.one(), match=match_2_query.one(),
            master_type=<'video' or 'audio'>,
            score=<score>, scaled_score=<scaled_score>,
            track_seek=<track_seek>, match_seek=<match_seek>,
        ))

    # Now we can query. Let's say the master_type was 'video' and the
    # scaled_scores were 0.8 and 0.9
    track = track_query.one()
    best, *rest = track.video_master_matches
    assert best.match == match_2_query.one()
    assert match_1_query.one().audio_candidate_matches[0].track == track

To get the top n matches for a track:
    def get_top_n(url_id, n, master_type):
        video = session.query(Video).filter_by(url_id=url_id).one_or_none()
        if not video:
            return None
        if master_type == 'video':
            return video.video_master_maches.limit(n)
        else:
            return video.audio_master_matches.limit(n)
"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from settings import user, password, host, port, database


metadata = sa.MetaData(schema='tft')
Base = declarative_base(metadata=metadata)

sa.event.listen(
    Base.metadata,
    'before_create',
    sa.DDL(
        'ALTER DATABASE tft SET TIMEZONE TO "UTC";'
        'CREATE SCHEMA IF NOT EXISTS public;'
        'CREATE SCHEMA IF NOT EXISTS tft;'
        'CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA pg_catalog;'
    ),
)


def create_engine():
    connection_string = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
        user, password, host, port, database)
    return sa.create_engine(connection_string)


def _match_relationship(track_or_match, video_or_audio):
    return relationship(
        'TrackMatch',
        primaryjoin=(
            "and_(Video.id==TrackMatch.{}_id,"
            " TrackMatch.master_type=='{}')".format(
                track_or_match, video_or_audio
            )
        ),
        order_by='desc(TrackMatch.scaled_score)',
        lazy='dynamic',
    )


def _time_track(name):
    return sa.Column(
        pg.ARRAY(pg.NUMERIC),
        sa.CheckConstraint(
            'COALESCE(ARRAY_LENGTH({}, 1), 0) > 0'.format(name)
        ),
        sa.CheckConstraint(
            '0 < ALL({})'.format(name)
        ),
        sa.CheckConstraint(
            'duration > ALL({})'.format(name)
        ),
        # These don't work...
        #sa.CheckConstraint(
        #    '{name} = sort({name})'.format(name=name)
        #),
        #sa.CheckConstraint(
        #    '{name} = uniq({name})'.format(name=name)
        #),
        nullable=False,
    )


class Video(Base):
    __tablename__ = 'video'
    id = sa.Column(
        pg.UUID, primary_key=True, server_default=func.uuid_generate_v4())
    url_id = sa.Column(pg.TEXT, unique=True, nullable=False)
    duration = sa.Column(pg.NUMERIC, nullable=False)
    video_shot_times = _time_track('video_shot_times')
    audio_beat_times = _time_track('audio_beat_times')
    video_metadata = sa.Column(
        pg.json.JSONB,
        sa.CheckConstraint(
            "video_metadata @> '{}'",
            name='video_metadata_valid_json_check',
        ),
        nullable=False,
        server_default='{}',
    )

    video_master_matches = _match_relationship('track', 'video')
    audio_master_matches = _match_relationship('track', 'audio')
    video_candidate_matches = _match_relationship('match', 'audio')
    audio_candidate_matches = _match_relationship('match', 'video')

    __table_args__ = (
        sa.UniqueConstraint('id', 'duration'),
    )


class TrackMatch(Base):
    __tablename__ = 'track_match'
    track_match_id = sa.Column(
        pg.UUID, primary_key=True, server_default=func.uuid_generate_v4()
    )

    track_id = sa.Column(pg.UUID, nullable=False)
    track_duration = sa.Column(pg.NUMERIC, nullable=False)
    track = relationship('Video', foreign_keys=(track_id, track_duration))

    match_id = sa.Column(pg.UUID, nullable=False)
    match_duration = sa.Column(pg.NUMERIC, nullable=False)
    match = relationship('Video', foreign_keys=(match_id, match_duration))

    master_type = sa.Column(
        pg.ENUM('video', 'audio', name='master_enum'), nullable=False)

    score = sa.Column(
        sa.Integer,
        sa.CheckConstraint('score > 0'),
        nullable=False,
    )
    scaled_score = sa.Column(
        pg.NUMERIC,
        sa.CheckConstraint('(scaled_score > 0) AND (scaled_score <= 1)'),
        nullable=False,
    )
    track_seek = sa.Column(
        pg.NUMERIC,
        sa.CheckConstraint(
            '(track_seek >= 0) AND (track_seek < track_duration)'),
        nullable=False,
    )
    match_seek = sa.Column(
        pg.NUMERIC,
        sa.CheckConstraint(
            '(match_seek >= 0) AND (match_seek < match_duration)'),
        nullable=False,
    )

    __table_args__ = (
        sa.ForeignKeyConstraint(
            ('track_id', 'track_duration'),
            ('video.id', 'video.duration'),
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        sa.ForeignKeyConstraint(
            ('match_id', 'match_duration'),
            ('video.id', 'video.duration'),
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        sa.CheckConstraint('track_id != match_id'),
        sa.UniqueConstraint('track_id', 'match_id', 'master_type'),
    )
