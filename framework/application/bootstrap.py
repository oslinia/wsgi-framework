from collections.abc import Generator
from datetime import datetime, timezone
from typing import Any

from . import StartResponse, Environment, Application
from .http.call import Response
from .http.call.response import Head
from .resource import initialization
from ..http import utc


class Bootstrap(object):
    __slots__ = ()

    def __init__(self: Application, import_name: str):
        initialization(import_name)

    def __call__(self, environ: Environment, start_response: StartResponse) -> Generator[bytes, Any, None]:
        utc.now = datetime.now(timezone.utc)
        utc.timestamp = utc.now.timestamp()

        Head.cookie = dict()
        Head.simple = dict()

        return Response(environ)(start_response)
