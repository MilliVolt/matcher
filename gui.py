#!/usr/bin/env python3
"""TFT gui."""
import tornado.ioloop
import tornado.web

from youtube_dl import YoutubeDL


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        video_id = self.get_argument('v')
        with YoutubeDL() as ydl:
            info = ydl.extract_info(video_id, download=False)
        vid_url, aud_url = (url['url'] for url in info['requested_formats'])
        self.render('watch.html', video_url=vid_url, audio_url=aud_url)


if __name__ == '__main__':
    tornado.web.Application(
        [
            (r'/watch', MainHandler),
        ],
        template_path='templates',
    ).listen(8888)
    tornado.ioloop.IOLoop.current().start()
