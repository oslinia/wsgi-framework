import os
from datetime import timedelta

from framework.http import utc, Path, Http


class Handler(Http):
    __slots__ = ()

    def __call__(self, code: int):
        return self.response(f"Error: {code}", code=code)


class Index(Http):
    __slots__ = ()

    def __call__(self):
        self.http.header('page', 'Index')
        # print(utc.now + timedelta(hours=3))
        self.set_cookie('name', 'value', expires=utc.now + timedelta(hours=4))
        # self.set_cookie('name', expires=0)

        return self.response(f"cookie: {self.cookie('name')}")


class Query(Http):
    __slots__ = ()

    def __call__(self):
        return self.response(f"Query: {self.query('query')} {self.query('key')}")


class Media(Http):
    __slots__ = ()

    def __call__(self, path: Path):
        file = self.file_path(path['name'])

        if os.path.isfile(file):
            return self.http.media(file)

        return 'File not found', 404, None, 'ascii'


class Page(Http):
    __slots__ = ()

    def __call__(self, path: Path):
        return self.render_template(f"page/{path['name']}", dict(title=path['name'][:-5], name=path['name']))


class Redirect(Http):
    __slots__ = ()

    def index(self):
        return self.render_template('page/redirect.html', dict(title='Redirect'))

    def __call__(self, path: Path):
        url = self.url_for('page', name=path['name'])

        return self.redirect_response(url)


class Archive(Http):
    __slots__ = ()

    def __call__(self, path: Path):
        self.charset('ascii')
        self.http.header('header', 'Archive')

        print(self.url_path('style.css'))
        print(self.url_for('index'))
        print(self.url_for('query'))
        print(self.url_for('error'))
        print(self.url_for('page', name='index.html'))
        print(self.url_for('archive', year='2025', month='02', day='23', error='23'))
        print(self.url_for('archive', year='2025', month='02', error='23'))
        print(self.url_for('archive', year='2025', month='02', day='23'))
        print(self.url_for('archive', year='2025', month='02'))

        return self.response(f"Archive {path}")
