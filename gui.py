#!/usr/bin/env python3
"""TFT gui."""
import pafy

from sqlalchemy.orm import sessionmaker
import tornado.ioloop
import tornado.web
from tornado.web import url

import models


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        tracks = pafy.new(self.get_argument('v'))
        self.render(
            'watch.html',
            video_url=tracks.getbestvideo().url,
            video_seek=self.get_argument('vseek', 0),
            audio_url=tracks.getbestaudio().url,
            audio_seek=self.get_argument('aseek', 0),
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
