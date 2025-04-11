import os.path

from framework.http import header, url_for, redirect, response, template, Path, Http


class Handler(Http):
    __slots__ = ()

    def __call__(self, code: int):
        return self.response(f"Error: {code}", code=code)


def index():
    header('name', 'Value')

    return response('Index')


class Query(Http):
    __slots__ = ()

    def __call__(self):
        return self.response(f"Query: {self.query('query')} {self.query('key')}")


class Media(Http):
    __slots__ = ()

    def __call__(self, path: Path):
        file = self.to_media(path['name'])

        if os.path.isfile(file):
            return self.media(file)

        else:
            return b'File not found', 404, None, 'ascii'


class Redirect(object):
    __slots__ = ()

    @classmethod
    def index(cls):
        return template('redirect/index.html', dict(title='Redirect'))

    def __call__(self, path: Path):
        return redirect(url_for('page', name=path['name']))


class Page(Http):
    __slots__ = ()

    def __call__(self, path: Path):
        print(self.url_path('style.css'))
        print(self.url_for('index'))
        print(self.url_for('query'))
        print(self.url_for('error'))
        print(self.url_for('page', name='index.html'))
        print(self.url_for('archive', year='2025', month='02', day='23', error='23'))
        print(self.url_for('archive', year='2025', month='02', error='23'))
        print(self.url_for('archive', year='2025', month='02', day='23'))
        print(self.url_for('archive', year='2025', month='02'))
        return self.template(f"page/{path['name']}", dict(title=path['name'][:-5], name=path['name']))


class Archive(Http):
    __slots__ = ()

    def __call__(self, path: Path):
        self.charset('ascii')
        # charset('ascii')
        self.header('head', 'Archive')

        return self.response(f"Archive {path}")
