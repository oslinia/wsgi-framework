import re

from typing import Any

from .. import routing

template_lang: str


def init(context: dict[str, Any] | None):
    html: dict[str, Any] = {
        'lang': template_lang,
    }

    if context is not None:
        html.update(context)

    return html


def from_string(value: str, args: tuple[str, ...]):
    for arg in args:
        value = getattr(value, arg)()

    return value


class Engine(object):
    __slots__ = 'context', 'args'

    def __init__(self, context: dict[str, Any] | None):
        self.context = init(context)

    @property
    def url_path(self):
        return f"{routing.static_urlpath}{self.args.strip(r'\'"')}"

    @property
    def url_for(self):
        name, *args = (v.lstrip() if '=' in v else v.strip(r'\'"') for v in self.args.split(','))

        if routing.link.has(name):
            length, details = len(args), routing.link.get(name)

            if length in details:
                mask, pattern = details[length]

                for k, v in (a.split('=') for a in args):
                    mask = mask.replace(f"{{{k}}}", v.strip(r'\'"'))

                if match := re.fullmatch(pattern, mask):
                    return match.string

        return None

    def __call__(self, fragment: str):
        value, name, *args = None, *(e.strip() for e in re.split(r'\|', fragment[2:-2]))

        if '(' in name:
            method, self.args = (e.strip() for e in name[:-1].split('('))

            if method in ('url_path', 'url_for'):
                value = getattr(self, method)

        if name in self.context:
            return from_string(self.context[name], args)

        return '' if value is None else value
