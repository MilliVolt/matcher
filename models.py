"""Postgres"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.ext.declarative import declarative_base
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


class Video(Base):
    __tablename__ = 'video'
    id = sa.Column(
        pg.UUID, primary_key=True, server_default=func.uuid_generate_v4())
    url_id = sa.Column(pg.TEXT, unique=True, nullable=False)
    duration = sa.Column(pg.NUMERIC, nullable=False)
    video_metadata = sa.Column(
        pg.json.JSONB,
        sa.CheckConstraint(
            "video_metadata @> '{}'",
            name='video_metadata_valid_json_check',
        ),
        nullable=False,
        server_default='{}',
    )

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
    match_id = sa.Column(pg.UUID, nullable=False)
    match_duration = sa.Column(pg.NUMERIC, nullable=False)
    match_type = sa.Column(
        pg.ENUM('video', 'audio', name='av_enum'), nullable=False)
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
        sa.UniqueConstraint('track_id', 'match_id', 'match_type'),
    )
