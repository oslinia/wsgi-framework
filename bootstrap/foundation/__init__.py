from collections.abc import Callable, Generator
from types import TracebackType
from typing import Any, Protocol, TypeAlias

Headers: TypeAlias = list[tuple[str, str]]

_ExcInfo: TypeAlias = tuple[type[BaseException], BaseException, TracebackType]
_OptExcInfo: TypeAlias = _ExcInfo | tuple[None, None, None]


class StartResponse(Protocol):
    def __call__(
            self,
            status: str,
            headers: Headers,
            exc_info: _OptExcInfo | None = ...,
            /,
    ) -> Callable[[bytes], object]: ...


Environment: TypeAlias = dict[str, Any]
Application: TypeAlias = Callable[[Environment, StartResponse], Generator[bytes, Any, None]]
