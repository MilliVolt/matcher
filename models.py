"""Postgres stuff."""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func

from settings import user, password, host, port, database


metadata = sa.MetaData(schema='tft')
Base = declarative_base(metadata=metadata)

sa.event.listen(
    Base.metadata,
    'before_create',
    sa.DDL("""
        ALTER DATABASE tft SET TIMEZONE TO "UTC";
        CREATE SCHEMA IF NOT EXISTS public;
        CREATE SCHEMA IF NOT EXISTS tft;
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA pg_catalog;
    """),
)


def create_engine():
    connection_string = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
        user, password, host, port, database)
    return sa.create_engine(connection_string)


videotag = sa.Table(
    'videotag', metadata,
    sa.Column(
        'videotag_video_id', pg.UUID, sa.ForeignKey('video.video_id'),
        nullable=False,
    ),
    sa.Column(
        'videotag_tag_id', pg.UUID, sa.ForeignKey('tag.tag_id'),
        nullable=False,
    ),
    sa.UniqueConstraint('videotag_video_id', 'videotag_tag_id'),
)


class Video(Base):
    __tablename__ = 'video'
    video_id = sa.Column(
        pg.UUID, primary_key=True, server_default=func.uuid_generate_v4())
    url_id = sa.Column(pg.TEXT, unique=True, nullable=False)
    title = sa.Column(pg.TEXT, nullable=False)
    duration = sa.Column(pg.NUMERIC, nullable=False)
    audio_beat_times = sa.Column(
        pg.ARRAY(pg.NUMERIC),
        sa.CheckConstraint(
            'COALESCE(ARRAY_LENGTH(audio_beat_times, 1), 0) > 0',
            name='video_audio_beat_times_not_empty',
        ),
        sa.CheckConstraint(
            '0 <= ALL(audio_beat_times)',
            name='video_audio_beat_times_all_nonnegative',
        ),
        sa.CheckConstraint(
            '(duration + 1) >= ALL(audio_beat_times)',
            name='video_audio_beat_times_lessequal_duration',
        ),
        nullable=False,
    )
    tags = relationship(
        'Tag', secondary=videotag, back_populates='videos', lazy='dynamic')

    @validates('audio_beat_times')
    def validate_audio_beat_times(self, key, abt):
        if abt != sorted(set(abt)):
            raise ValueError('Times must be sorted and unique.')
        return abt

    video_metadata = sa.Column(
        pg.JSONB,
        sa.CheckConstraint(
            "video_metadata @> '{}'",
            name='video_metadata_valid_json_check',
        ),
        nullable=False,
        server_default='{}',
    )

    __table_args__ = (
        sa.UniqueConstraint('video_id', 'duration'),
    )


class Tag(Base):
    __tablename__ = 'tag'
    tag_id = sa.Column(
        pg.UUID, primary_key=True, server_default=func.uuid_generate_v4())
    tag_name = sa.Column(pg.TEXT, nullable=False)
    videos = relationship(
        'Video', secondary=videotag, back_populates='tags', lazy='dynamic')

    __table_args__ = (
        sa.Index('lowercase_tag_name', func.lower(tag_name), unique=True),
    )


class AudioSwap(Base):
    __tablename__ = 'audioswap'
    audioswap_id = sa.Column(
        pg.UUID, primary_key=True, server_default=func.uuid_generate_v4()
    )

    from_id = sa.Column(pg.UUID, nullable=False)
    from_duration = sa.Column(pg.NUMERIC, nullable=False)
    from_audio = relationship('Video', foreign_keys=(from_id, from_duration))

    to_id = sa.Column(pg.UUID, nullable=False)
    to_duration = sa.Column(pg.NUMERIC, nullable=False)
    to_audio = relationship('Video', foreign_keys=(to_id, to_duration))

    score = sa.Column(
        sa.Integer,
        sa.CheckConstraint('score > 0', name='audioswap_score_greater_0'),
        nullable=False,
    )
    scaled_score = sa.Column(
        pg.NUMERIC,
        nullable=False,
    )
    from_seek = sa.Column(
        pg.NUMERIC,
        sa.CheckConstraint(
            '(from_seek >= 0) AND (from_seek <= from_duration + 1)',
            name='audioswap_from_seek_within_bounds'
        ),
        nullable=False,
    )
    to_seek = sa.Column(
        pg.NUMERIC,
        sa.CheckConstraint(
            '(to_seek >= 0) AND (to_seek <= to_duration + 1)',
            name='audioswap_to_seek_within_bounds'
        ),
        nullable=False,
    )

    __table_args__ = (
        sa.ForeignKeyConstraint(
            ('from_id', 'from_duration'),
            ('video.video_id', 'video.duration'),
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        sa.ForeignKeyConstraint(
            ('to_id', 'to_duration'),
            ('video.video_id', 'video.duration'),
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        sa.CheckConstraint('from_id != to_id', name='audioswap_diff_videos'),
        sa.UniqueConstraint('from_id', 'to_id'),
        sa.Index('best_from_swap_index', from_id, scaled_score.desc()),
        sa.Index('best_to_swap_index', to_id, scaled_score.desc()),
    )


def get_video(session, *, url_id, none=True):
    query = session.query(Video).filter_by(url_id=url_id)
    return query.one_or_none() if none else query.one()


def _pick_value(value, possibilities, choices):
    try:
        index = possibilities.index(value)
    except ValueError:
        raise ValueError("'{}' not in {}".format(value, possibilities))
    return (c[index] for c in choices)


def get_best_matches(
        session, *, video,
        from_or_to='from', scaled_or_absolute_score='scaled', tags=None):
    """Get matches for a video."""
    joiner, filterer = _pick_value(
        from_or_to,
        ('from', 'to'),
        (
            (AudioSwap.to_id, AudioSwap.from_id),
            (AudioSwap.from_id, AudioSwap.to_id),
        )
    )
    orderer, = _pick_value(
        scaled_or_absolute_score,
        ('scaled', 'absolute'),
        ((AudioSwap.scaled_score, AudioSwap.score),)
    )
    query = (
        session.query(AudioSwap)
        .join(Video, joiner == Video.video_id)
        .filter(filterer == video.video_id)
        .filter(AudioSwap.scaled_score >= 0.3)
    )
    if tags:
        query = query.filter(video.tags.any(tag.tag_name.in_(tags)))

    return query.order_by(orderer.desc()).limit(40)


def get_unmatched(session, *, limit=2000):
    # Would be good to use TABLESAMPLE here... postgres >= 9.5
    sql = sa.text("""
        select x.video_id as from_id, y.video_id as to_id
        from (select video_id from tft.video) x
        join (select video_id from tft.video) y
        on x.video_id != y.video_id
        and not exists (
            select 1 from tft.audioswap
            where tft.audioswap.from_id = x.video_id
            and tft.audioswap.to_id = y.video_id
        )
        and y.video_id in (
            select video_id from tft.video order by random() limit 10
        )
        limit :limit;""")
    return session.bind.execute(sql, limit=limit)
