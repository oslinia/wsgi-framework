import os
from datetime import timedelta

from bootstrap.http import charset, response, Path, Http
from bootstrap.utils import utc


class Handler(object):
    __slots__ = ()

    def __call__(self, code: int):
        charset('ascii')

        return response(f"Error: {code}", code=code)


class Page(Http):
    __slots__ = ()

    def index(self):
        self.set_cookie('name', 'value', expires=utc.now + timedelta(hours=3), samesite='Strict')
        # self.delete_cookie('name')
        return self.response(f"Index page, cookie: {self.cookie('name')}")

    def url(self):
        return self.response(f"Query: {self.query('query')} {self.query('key')}")

    def static(self, path: Path):
        file = os.path.join(self.http.routing.dirname, 'resource', 'static', path['name'])

        if os.path.isfile(file):
            return self.http.media(file)

        return 'File not found', 404, None, 'ascii'

    def __call__(self, path: Path):
        return self.template(f"page/{path['name']}", dict(title=path['name'][:-5], name=path['name']))


class Redirect(Http):
    __slots__ = ()

    def index(self):
        return self.template('template/redirect.html')

    def __call__(self, path: Path):
        return self.redirect(self.url_for('page', name=path['name']))


class Archive(Http):
    __slots__ = ()

    def __call__(self, path: Path):
        self.charset('ascii')
        self.http.response.header('header', 'Archive')

        print(self.url_path('style.css'))
        print(self.url_for('index'))
        print(self.url_for('error'))
        print(self.url_for('query'))
        print(self.url_for('static', name='style.css'))
        print(self.url_for('page', name='index.html'))
        print(self.url_for('archive', year='2025', month='02'))
        print(self.url_for('archive', year='2025', month='02', day='23', error='23'))
        print(self.url_for('archive', year='2025', month='02', error='23'))
        print(self.url_for('archive', year='2025', month='02', day='23'))

        return self.response(f"Archive {path}")
