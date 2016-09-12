#!/usr/bin/env python3
"""TFT gui."""
import pafy

from sqlalchemy.orm import sessionmaker
import tornado.ioloop
import tornado.web
from tornado.web import url

import models


class BaseHandler(tornado.web.RequestHandler):
    @property
    def session(self):
        return self.application.session


class MainHandler(BaseHandler):
    def get(self):
        url_id = self.get_argument('v')
        video = models.get_video(self.session, url_id=self.get_argument('v'))
        if not video:
            best_match = None
            #raise tornado.web.HTTPError(404)
        else:
            tags = self.get_argument('tags', [])
            if tags:
                tags = tags.split(',')
            best_matches = models.get_best_matches(self.session, video=video,
                tags=tags)
        audio_url = None
        video_seek = None
        audio_seek = None
        if best_matches.count():
            best_match = best_matches[0]
            video_seek = best_match.track_seek
            audio_seek = best_match.match_seek
            audio_url_id = best_match.match.url_id
            audio_url = pafy.new(audio_url_id).getbestaudio().url
        self.render(
            'watch.html',
            video_url=pafy.new(url_id).getbestvideo().url,
            audio_url=audio_url or pafy.new(url_id).getbestaudio().url,
            video_seek=video_seek or self.get_argument('vseek', '0'),
            audio_seek=audio_seek or self.get_argument('aseek', '0'),
        )


class Application(tornado.web.Application):
    def __init__(self):
        settings = {
            'static_path': 'static',
            'template_path': 'templates',
        }
        urls = [
            url(r'/watch', MainHandler),
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
