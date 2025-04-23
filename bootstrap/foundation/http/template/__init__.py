import os
import re

from typing import Any

from .engine import Engine

templates_folder: str


def path_to(name: str):
    file = os.path.realpath(os.path.join(templates_folder, name))

    if os.path.isfile(file):
        return file

    return None


def each_fragment(file: str):
    with open(file) as f:
        for fragment in re.split(r'({%.*?%}|{{.*?}})', f.read()):
            if fragment:
                yield fragment


class Template(object):
    __slots__ = 'key', 'name', 'map', 'list', 'engine'

    def append(self, fragment: str):
        self.list.append(fragment)

        self.key += 1

    def edit(self, fragment: str):
        key = self.map[self.name]

        self.list[key] = f"{self.list[key]}{fragment.strip('\n')}"

    def extends(self, name: str):
        file = path_to(name.strip(r'\'"'))

        if file is not None:
            self.compile(file)

    def block(self, name: str):
        self.name = name

        if name in self.map:
            key = self.map[self.name]

            self.list[key] = ''

        else:
            self.map.update({name: self.key})

            self.append('')

    def template(self, value, *args):
        match value:
            case 'extends':
                self.extends(*args)

            case 'block':
                self.block(*args)

            case _:
                self.name = None

    def string(self, fragment: str):
        if self.name is None:
            self.append(fragment)

        else:
            self.edit(fragment)

    def compile(self, file: str):
        for fragment in each_fragment(file):
            match fragment[:2]:
                case '{%':
                    self.template(*re.split(r'\s+', fragment[2:-2].strip()))

                case '{{':
                    self.string(self.engine(fragment))

                case _:
                    self.string(fragment)

    def __init__(self, name: str, context: dict[str, Any] | None):
        file = path_to(name)

        if file is None:
            self.key = None

        else:
            self.key, self.name, self.map, self.list = 0, None, dict(), list()

            self.engine = Engine(context)

            self.compile(file)

    def __call__(self, code: int | None, mimetype: str, encoding: str | None):
        if self.key is None:
            return b'Template not found', 500, None, 'ascii'

        body: str = ''.join(self.list).strip()

        return body, code, mimetype, encoding
