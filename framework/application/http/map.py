import os
import re
from typing import Any


def mapper(file: str, dirname: str, import_name: str):
    cache = not os.path.isfile(file)

    if cache:
        setattr(Map, 'rules', dict())

    for name, value in (
            ('error', None),
            ('cache', cache),
            ('endpoints', dict()),
    ):
        setattr(Map, name, value)

    if os.path.isfile(f"{dirname}{os.sep}app{os.sep}main.py"):
        __import__(f"{import_name}app.main")

    return cache


class Map(object):
    __slots__ = 'error', 'cache', 'rules', 'endpoints'

    error: tuple[str, str, str | None] | None
    cache: bool
    rules: dict[str, str | tuple[str, dict[str, str]]]
    endpoints: dict[str, tuple[tuple[str, str, str | None], tuple[tuple[Any, ...], dict[str, Any]] | None]]


class Mapper(Map):
    __slots__ = 'patterns', 'masks', 'links', 'where'

    patterns: list[tuple[str, str]]
    masks: dict[str, list[tuple[int, tuple[str, ...]] | None]]
    links: dict[str, list[tuple[int, str, str]]]

    def pattern(self, mask: str):
        if self.where is not None and mask in self.where:
            return self.where[mask]

        return '[A-Za-z0-9_-]+'

    def __init__(self):
        self.patterns, self.masks, self.links = list(), dict(), dict()

        for path, items in self.rules.items():
            pattern = link = path

            if isinstance(items, str):
                name, self.where = items, None

            else:
                name, self.where = items

            if masks := tuple(re.findall(r'{([A-Za-z0-9_-]+)}', path)):
                for mask in masks:
                    pattern = pattern.replace(f"{{{mask}}}", f"({self.pattern(mask)})")
                    link = link.replace(f"{{{mask}}}", self.pattern(mask))

                num = len(masks)

                where = num, masks

            else:
                num = 0

                where = None

            self.patterns.append((f"^{pattern}\\Z", name))

            if name in self.masks:
                self.masks[name].append(where)

            else:
                self.masks[name] = where if where is None else [where]

            if name in self.links:
                self.links[name].append((num, path, link))

            else:
                self.links[name] = [(num, path, link)]
