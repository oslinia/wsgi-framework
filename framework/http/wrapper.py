from typing import Any

from ..application import http


class Path(dict[str, str]):
    def __init__(self, **kwargs: str):
        super().__init__(kwargs)


class Http(object):
    __slots__ = 'http',

    def __init__(self):
        self.http = http

    def query(self, name: str):
        return self.http.query.get(name)

    def cookie(self, name: str):
        return self.http.cookie.get(name)

    def form(self, name: str):
        return self.http.form.data.get(name)

    def upload(self, name: str):
        return self.http.form.upload.get(name)

    def header(self, name: str, value: str):
        self.http.header.simple[name] = value

    def has(self, name: str):
        return name in self.http.header.simple

    def delete(self, name: str):
        if name in self.http.header.simple:
            del self.http.header.simple[name]

    def set_cookie(self, name: str, value: str):
        pass

    def to_media(self, name: str):
        return self.http.to_media(name)

    def media(self, file: str):
        return self.http.media(file)

    def url_path(self, name: str):
        return self.http.urlpath(name)

    def url_for(self, *args: str, **kwargs: str):
        return self.http.link(args, kwargs)

    def redirect(self, url: str, code=307):
        return self.http.redirect(url, code)

    def charset(self, encoding: str):
        self.http.encoding = encoding

    def response(
            self,
            body: bytes | str,
            *,
            code: int = None,
            mimetype: str = None,
    ):
        return body, code, mimetype, self.http.encoding

    def template(
            self,
            name: str,
            context: dict[str, Any] = None,
            *,
            code: int = None,
            mimetype: str = 'text/html',
    ):
        return self.http.Template(name, context)(code, mimetype, self.http.encoding)
