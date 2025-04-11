from typing import Any

from .wrapper import http, Path, Http


def query(name: str):
    return http.query.get(name)


def cookie(name: str):
    return http.cookie.get(name)


def form(name: str):
    return http.form.data.get(name)


def upload(name: str):
    return http.form.upload.get(name)


def header(name: str, value: str):
    http.header.simple[name] = value


def has(name: str):
    return name in http.header.simple


def delete(name: str):
    if name in http.header.simple:
        del http.header.simple[name]


def set_cookie(name: str, value: str):
    pass


def to_media(name: str):
    return http.to_media(name)


def media(file: str):
    return http.media(file)


def url_path(name: str):
    return http.urlpath(name)


def url_for(*args: str, **kwargs: str):
    return http.link(args, kwargs)


def redirect(url: str, code=307):
    return http.redirect(url, code)


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
