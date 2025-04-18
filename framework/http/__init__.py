import os
from datetime import datetime, timedelta
from typing import Literal, Any

from ..application import http


class Path(dict[str, str]):
    def __init__(self, **kwargs: str):
        super().__init__(kwargs)


class Http(object):
    __slots__ = 'http',

    def __init__(self):
        self.http = http

    def file_path(self, name: str):
        return os.path.join(self.http.dirname, 'resource', 'media', name)

    def url_path(self, name: str):
        return f"{self.http.static_urlpath}{name}"

    def url_for(self, *args: str, **kwargs: str):
        return self.http.link.build(args, kwargs)

    def query(self, name: str):
        return self.http.query.get(name)

    def cookie(self, name: str):
        return self.http.cookie.get(name)

    def form(self, name: str):
        return self.http.form.data.get(name)

    def upload(self, name: str):
        return self.http.form.upload.get(name)

    def set_cookie(
            self,
            name: str,
            value: str = None,
            domain: str = None,
            path: str = '/',
            expires: datetime | float | int | str = None,
            max_age: timedelta | int = None,
            httponly: bool = False,
            secure: bool = False,
            samesite: Literal['Lax', 'None', 'Strict'] = None,
    ):
        self.http.cookies(name, value, domain, path, expires, max_age, httponly, secure, samesite)

    def charset(self, encoding: str):
        self.http.encoding = encoding

    def render_template(
            self,
            name: str,
            context: dict[str, Any] = None,
            *,
            code: int = None,
            mimetype: str = 'text/html',
    ):
        return self.http.Template(name, context)(code, mimetype, self.http.encoding)

    def response(
            self,
            body: bytes | str,
            *,
            code: int = None,
            mimetype: str = None,
    ):
        return body, code, mimetype, self.http.encoding

    def redirect_response(self, url: str, code=307):
        self.http.header('location', url)

        return b'', code, None, 'ascii'
