import os
from datetime import timezone
from zoneinfo import ZoneInfo

from .. import http
from ..http import template, Link
from ..http.call.response import Http
from ...http import utc


def set_timezone(zone: str):
    utc.tz = timezone.utc if 'utc' == zone.lower() else ZoneInfo(zone)


def configure(links: dict[str, dict[int, tuple[str, str]]], dirname: str, import_name: str):
    http.link = Link(links)

    http.dirname = dirname

    module = __import__(f"{import_name}resource.config", fromlist=['*'])

    http.static_urlpath = module.static_urlpath

    Http.encoding = module.encoding
    Http.block_size = module.block_size

    set_timezone(module.time_zone)

    template.engine.template_lang = module.template_lang
    template.templates_folder = os.path.realpath(f"{dirname}{os.sep}{module.templates_folder}")
