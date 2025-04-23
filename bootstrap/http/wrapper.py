from datetime import datetime, timedelta
from typing import Any, Literal

from ..foundation import http


class Path(dict[str, str]):
    def __init__(self, **kwargs: str):
        super().__init__(kwargs)


class Http(object):
    __slots__ = 'http',

    def __init__(self):
        self.http = http

    def url_path(self, name: str):
        return f"{self.http.routing.static_urlpath}{name}"

    def url_for(self, *args: str, **kwargs: str):
        name, = args

        return self.http.routing.link.build(name, kwargs)

    def query(self, name: str):
        return self.http.request.query.get(name)

    def cookie(self, name: str):
        return self.http.request.cookie.get(name)

    def form(self, name: str):
        return self.http.request.form.data.get(name)

    def upload(self, name: str):
        return self.http.request.form.upload.get(name)

    def set_cookie(
            self,
            name: str,
            value: str,
            *,
            domain: str = None,
            path='/',
            expires: datetime | float | int | str = None,
            max_age: timedelta | int = None,
            httponly=False,
            secure=False,
            samesite: Literal['Lax', 'None', 'Strict'] = None,
    ):
        self.http.response.cookie(name, value, domain, path, expires, max_age, httponly, secure, samesite)

    def delete_cookie(self, name: str, domain: str = None, path='/'):
        args = path, 0, None, False, False, None

        self.http.response.cookie(name, '', domain, *args)

    def redirect(self, url: str, code=307):
        self.http.response.header('location', url)

        return b'', code, None, 'ascii'

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
        return self.http.Template(name, context)(code, mimetype, http.encoding)
