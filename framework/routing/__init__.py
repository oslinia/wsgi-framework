from typing import Any

from .map import Error, Rule, Endpoint


def callback(obj: Any, method: str = None):
    return obj.__module__, obj.__name__, method
