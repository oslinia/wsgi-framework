import re
from typing import Any

from .map import Map
from ....http import Path

link: "Link"

dirname: str
static_urlpath: str


class Link(object):
    __slots__ = '__links',

    def __init__(self, links: dict[str, dict[int, tuple[str, str]]]):
        self.__links = links

    def has(self, name: str):
        return name in self.__links

    def get(self, name: str):
        return self.__links[name]

    def build(self, name: str, kwargs: dict[str, str]):
        if self.has(name):
            length, details = len(kwargs), self.get(name)

            if length in details:
                mask, pattern = details[length]

                for k, v in kwargs.items():
                    mask = mask.replace(f"{{{k}}}", v)

                if match := re.fullmatch(pattern, mask):
                    return match.string

        return None


def convert(body: bytes | str, code: int = None, mimetype: str = None, encoding: str = None):
    kwargs = dict()

    if code is not None:
        kwargs.update(code=code)

    if mimetype is not None:
        kwargs.update(mimetype=mimetype)

    if encoding is not None:
        kwargs.update(encoding=encoding)

    return body, kwargs


class Callback(object):
    __slots__ = 'object', 'method', 'args', 'kwargs'

    def type(self, args: tuple[Any, ...], kwargs: dict[str, Any]):
        call = self.object(*args)

        if self.method is not None:
            call = getattr(call, self.method)

        return call(**kwargs)

    def __init__(self, module: str, name: str, method: str = None):
        self.object, self.method = getattr(__import__(module, fromlist=[name]), name), method

    def __call__(self, *args, **kwargs):
        match self.object.__class__.__name__:
            case 'type':
                call = self.type(args, kwargs)

            case _:
                call = self.object(*args, **kwargs)

        if isinstance(call, bytes | str):
            return convert(call)

        return convert(*call)


class Routing(Map):
    __slots__ = 'patterns', 'masks', 'path'

    patterns: tuple[tuple[str, str], ...]
    masks: dict[str, dict[int, tuple[str, ...]] | None]

    path: dict[str, str] | None

    def arguments(self, middleware: tuple[tuple[Any, ...], dict[str, Any]] | None):
        args, kwargs = tuple(), dict() if middleware is None else middleware

        if self.path is not None:
            kwargs.update(path=Path(**self.path))

        return args, kwargs

    def endpoint(self, name: str):
        endpoint, middleware = self.endpoints[name]

        args, kwargs = self.arguments(middleware)

        return Callback(*endpoint)(*args, **kwargs)

    def route(self, name: str, values: str | tuple[str, ...]):
        self.path, masks = None, self.masks[name]

        if masks is not None:
            if isinstance(values, str):
                values = values,

            num = len(values)

            if num in masks:
                self.path = dict(zip(masks[num], values))

        if name in self.endpoints:
            return self.endpoint(name)

        return None

    def response(self, path: str):
        callback = None

        for pattern, name in self.patterns:
            if r := re.findall(pattern, path):
                callback = self.route(name, r[0])

                break

        if callback is None:
            if self.error is None:
                return convert(b'Not Found', 404, encoding='ascii')

            else:
                return Callback(*self.error)(code=404)

        return callback
