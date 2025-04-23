from datetime import datetime, timedelta
from typing import Any, Literal

from .wrapper import http, Path, Http


def url_path(name: str):
    return f"{http.routing.static_urlpath}{name}"


def url_for(*args: str, **kwargs: str):
    name, = args

    return http.routing.link.build(name, kwargs)


def query(name: str):
    return http.request.query.get(name)


def cookie(name: str):
    return http.request.cookie.get(name)


def form(name: str):
    return http.request.form.data.get(name)


def upload(name: str):
    return http.request.form.upload.get(name)


def set_cookie(
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
    http.response.cookie(name, value, domain, path, expires, max_age, httponly, secure, samesite)


def delete_cookie(name: str, domain: str = None, path='/'):
    args = path, 0, None, False, False, None

    http.response.cookie(name, '', domain, *args)


def redirect(url: str, code=307):
    http.response.header('location', url)

    return b'', code, None, 'ascii'


def charset(encoding: str):
    http.encoding = encoding


def response(
        body: bytes | str,
        *,
        code: int = None,
        mimetype: str = None,
):
    return body, code, mimetype, http.encoding


def template(
        name: str,
        context: dict[str, Any] = None,
        *,
        code: int = None,
        mimetype: str = 'text/html',
):
    return http.Template(name, context)(code, mimetype, http.encoding)
