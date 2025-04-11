import os
from datetime import timezone
from zoneinfo import ZoneInfo

from ..http import call, engine, routing, template
from ..http.call.response import Http
from ...utils import utc


def templates(dirname: str, folder: str):
    return os.path.realpath(f"{dirname}{os.sep}{folder}")


def set_timezone(zone: str):
    utc.tz = timezone.utc if 'utc' == zone.lower() else ZoneInfo(zone)


def configure(import_name: str, dirname: str):
    module = __import__(f"{import_name}resource.config", fromlist=['*'])

    Http.encoding = module.encoding
    Http.block_size = module.block_size

    call.dirname = dirname

    routing.static_urlpath = module.static_urlpath

    engine.template_lang = module.template_lang
    template.templates_folder = templates(dirname, module.templates_folder)

    set_timezone(module.time_zone)
