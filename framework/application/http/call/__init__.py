import os
from collections.abc import Generator

from .request import Query, Cookie, Form
from .response import Head, Media, Document
from ..routing import Routing
from ... import http, StartResponse, Environment

header = Head

dirname: str


def env(name: str):
    return request.env.get(name)


def to_media(name: str):
    return f"{dirname}{os.sep}resource{os.sep}media{os.sep}{name}"


def media(file: str):
    Response.flag = True

    return file


def redirect(url: str, code: int):
    Head.simple['location'] = url

    return b'', code, None, 'ascii'


class Response(Routing):
    __slots__ = 'flag', 'body', 'kwargs'

    def __init__(self, environ: Environment):
        Response.flag, request.env = False, environ

        for name, value in (
                ('query', Query(environ)),
                ('cookie', Cookie(environ)),
                ('form', Form(environ)),
                ('encoding', None),
        ):
            setattr(http, name, value)

        self.body, self.kwargs = self.response(environ['PATH_INFO'])

    def __call__(self, start_response: StartResponse) -> Generator[bytes, None, None]:
        if self.flag:
            return Media(self.body)(start_response)

        else:
            return Document(self.body, **self.kwargs)(start_response)
