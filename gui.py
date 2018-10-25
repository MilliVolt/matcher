#!/usr/bin/env python3
"""TFT gui."""
import pafy

from sqlalchemy import select, true
from sqlalchemy.orm import sessionmaker

import tornado.ioloop
import tornado.web
from tornado.web import url

import models


class BaseHandler(tornado.web.RequestHandler):
    @property
    def session(self):
        return self.application.session

class IndexHandler(BaseHandler):
    def get(self):
        subq = (
            select([models.AudioSwap])
            .where(models.AudioSwap.from_id == models.Video.video_id)
            .order_by(models.AudioSwap.scaled_score.desc())
            .limit(1)
            .lateral()
        )
        best_results = (
            self.session
            .query(models.AudioSwap)
            .select_entity_from(
                select([subq])
                .select_from(models.Video.__table__.join(subq, true()))
            )
            .filter(models.AudioSwap.scaled_score <= self.get_argument('max', 0.7))
            .filter(models.AudioSwap.scaled_score >= self.get_argument('min', 0.3))
            .order_by(models.AudioSwap.scaled_score.desc())
            .limit(self.get_argument('n', 100))
        )
        self.write(''.join('''
            {}<br><a href="/watch?v={}">{}</a><br>{}<br>
            sscore: {}<br>
            ascore: {}<br>
            <br>
        '''.format(
            i,
            match.from_audio.url_id, match.from_audio.video_metadata['title'],
            match.to_audio.video_metadata['title'],
            match.scaled_score, match.score
        ) for i, match in enumerate(best_results)))
        self.finish()



class MainHandler(BaseHandler):
    def get(self):
        url_id = self.get_argument('v')
        video = models.get_video(self.session, url_id=self.get_argument('v'))
        spec_audio_url_id = self.get_argument('a', None)
        best_matches_count = 0
        if not video:
            best_match = None
            #raise tornado.web.HTTPError(404)
        else:
            tags = self.get_argument('tags', [])
            if tags:
                tags = tags.split(',')
            best_matches = models.get_best_matches(self.session, video=video,
                tags=tags)
            best_matches_count = best_matches.count()
        audio_url = None
        video_seek = None
        audio_seek = None
        audio_url_id = None
        if best_matches_count:
            best_match = best_matches[0]
            video_seek = best_match.from_seek
            audio_seek = best_match.to_seek
            audio_url_id = best_match.to_audio.url_id
            audio_url = pafy.new(audio_url_id).getbestaudio().url
        if spec_audio_url_id:
            audio_url_id = spec_audio_url_id
            audio_url = pafy.new(audio_url_id).getbestaudio().url
        video_obj = pafy.new(url_id)
        self.render(
            'watch.html',
            video_title=video_obj.title,
            video_url=video_obj.getbestvideo().url,
            audio_title=pafy.new(audio_url_id or url_id).title,
            audio_url=audio_url or pafy.new(url_id).getbestaudio().url,
            video_url_id=url_id,
            audio_url_id=audio_url_id or url_id,
            backups = [] if not best_matches_count else best_matches,
            video_seek=self.get_argument('vseek', video_seek),
            audio_seek=self.get_argument('aseek', audio_seek),
        )


class ListHandler(BaseHandler):
    def get(self):
        # Maybe this should be the index view.
        results = (
            self.session
            .query(models.AudioSwap)
            .filter(models.AudioSwap.scaled_score <= self.get_argument('max', 0.7))
            .filter(models.AudioSwap.scaled_score >= self.get_argument('min', 0.3))
            .filter(models.AudioSwap.score >= 100)
            .order_by(models.AudioSwap.scaled_score.desc())
            .limit(self.get_argument('n', 100))
        )
        self.write(''.join('''
            {}<br><a href="/watch?v={}&a={}&vseek={}&aseek={}">{}</a><br>{}<br>
            sscore: {}<br>
            ascore: {}<br>
            <br>
        '''.format(
            i,
            match.from_audio.url_id, match.to_audio.url_id,
            match.from_seek, match.to_seek,
            match.from_audio.video_metadata['title'],
            match.to_audio.video_metadata['title'],
            match.scaled_score, match.score
        ) for i, match in enumerate(results)))
        self.finish()

class Application(tornado.web.Application):
    def __init__(self):
        settings = {
            'static_path': 'static',
            'template_path': 'templates',
        }
        urls = [
            url(r'/', IndexHandler),
            url(r'/watch', MainHandler),
            url(r'/list', ListHandler),
        ]
        super().__init__(urls, **settings)
        engine = models.create_engine()
        models.Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine, autocommit=True)
        self.session = Session()


if __name__ == '__main__':
    Application().listen(8888)
    print('Listening on port 8888')
    tornado.ioloop.IOLoop.current().start()
