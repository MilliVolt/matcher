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
        video = (
            self.session
            .query(models.Video)
            .filter_by(url_id=url_id)
            .one_or_none()
        )
        if not video:
            raise tornado.web.HTTPError(404)
        audio_url = None
        video_seek = None
        audio_seek = None
        if video.video_master_matches:
            best_match = video.video_master_matches[0]
            video_seek = best_match.track_seek
            audio_seek = best_match.match_seek
            audio_url_id = best_match.match.url_id
            audio_url = pafy.new(audio_url_id).getbestaudio().url
        self.render(
            'watch.html',
            video_url=pafy.new(url_id).getbestvideo().url,
            audio_url=audio_url,
            video_seek=video_seek,
            audio_seek=audio_seek,
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
