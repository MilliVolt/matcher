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
        user, password, host, port, database
    )
    return sa.create_engine(connection_string)


track_type_enum = sa.Enum(
    'video', 'audio', name='av_enum', inherit_schema=True
)


class Track(Base):
    __tablename__ = 'track'
    id = sa.Column(
        pg.UUID, primary_key=True, server_default=func.uuid_generate_v4()
    )
    url_id = sa.Column(pg.TEXT, nullable=False)
    track_type = sa.Column(track_type_enum, nullable=False)
    track_metadata = sa.Column(
        pg.json.JSONB,
        sa.CheckConstraint(
            "track_metadata @> '{}'",
            name='track_metadata_valid_json_check',
        ),
        nullable=False,
        server_default='{}',
    )

    __table_args__ = (
        sa.UniqueConstraint('url_id', 'track_type'),
        sa.UniqueConstraint('id', 'track_type'),
    )


class TrackMatch(Base):
    __tablename__ = 'track_match'
    track_match_id = sa.Column(
        pg.UUID, primary_key=True, server_default=func.uuid_generate_v4()
    )
    track_id = sa.Column(pg.UUID, nullable=False)
    track_type = sa.Column(track_type_enum, nullable=False)
    match_id = sa.Column(pg.UUID, nullable=False)
    match_type = sa.Column(track_type_enum, nullable=False)
    score = sa.Column(
        sa.Integer,
        sa.CheckConstraint('score > 0'),
        nullable=False,
    )
    scaled_score = sa.Column(
        pg.NUMERIC,
        sa.CheckConstraint('scaled_score > 0'),
        nullable=False,
    )
    track_seek = sa.Column(
        pg.NUMERIC,
        sa.CheckConstraint('track_seek >= 0'),
        nullable=False,
    )
    match_seek = sa.Column(
        pg.NUMERIC,
        sa.CheckConstraint('match_seek >= 0'),
        nullable=False,
    )

    __table_args__ = (
        sa.ForeignKeyConstraint(
            ['track_id', 'track_type'],
            ['track.id', 'track.track_type'],
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['match_id', 'match_type'],
            ['track.id', 'track.track_type'],
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        sa.CheckConstraint('track_id != match_id'),
        sa.CheckConstraint('track_type != match_type'),
        sa.UniqueConstraint('track_id', 'match_id'),
    )
