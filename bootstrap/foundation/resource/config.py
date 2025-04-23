import os
from datetime import timezone
from zoneinfo import ZoneInfo

from ..http import routing, template
from ..http.response import Http
from ..http.routing import Link
from ...utils import utc


def set_timezone(zone: str):
    utc.tz = timezone.utc if 'utc' == zone.lower() else ZoneInfo(zone)


def configuration(links: dict[str, dict[int, tuple[str, str]]], import_name: str, dirname: str):
    module = __import__(f"{import_name}resource.config", fromlist=['*'])

    Http.encoding = module.encoding
    Http.block_size = module.block_size

    set_timezone(module.time_zone)

    routing.link = Link(links)

    routing.dirname = dirname
    routing.static_urlpath = module.static_urlpath

    template.engine.template_lang = module.template_lang
    template.templates_folder = os.path.realpath(f"{dirname}{os.sep}{module.templates_folder}")
