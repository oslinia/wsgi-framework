from typing import Any

from ...foundation.http.routing import Map


class Error(object):
    __slots__ = ()

    def __init__(self, obj: Any, method: str = None):
        setattr(Map, 'error', (obj.__module__, obj.__name__, method))


class Rule(Map):
    __slots__ = 'path',

    def __init__(self, path: str, name: str):
        if self.cache:
            self.path = path

            self.rules[path] = name

    def where(self, **kwargs: str):
        if self.cache:
            self.rules[self.path] = self.rules[self.path], kwargs


class Endpoint(Map):
    __slots__ = 'name',

    def __init__(self, name: str, callback: tuple[str, str, str | None]):
        self.name = name

        self.endpoints[name] = callback, None

    def middleware(self, *args, **kwargs):
        self.endpoints[self.name] = self.endpoints[self.name][0], (args, kwargs)
