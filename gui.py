#!/usr/bin/env python3
"""TFT gui."""
import pafy

import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        tracks = pafy.new(self.get_argument('v'))
        self.render(
            'watch.html',
            video_url=tracks.getbestvideo().url,
            audio_url=tracks.getbestaudio().url,
        )


if __name__ == '__main__':
    tornado.web.Application(
        [
            (r'/watch', MainHandler),
        ],
        template_path='templates',
    ).listen(8888)
    tornado.ioloop.IOLoop.current().start()
