import mimetypes
import os
from collections.abc import Generator
from typing import Any

from ... import Headers, StartResponse


class Head(object):
    __slots__ = 'cookie', 'simple'

    cookie: dict[str, str]
    simple: dict[str, str]


class Http(Head):
    __slots__ = 'encoding', 'block_size', 'size', 'mimetype'

    encoding: str
    block_size: int

    def __init__(self, mimetype: str):
        self.size, self.mimetype = None, mimetype

    def iana(self, mimetype: str | None, encoding: str | None):
        if mimetype is None:
            mimetype = 'application/octet-stream'

        if mimetype.startswith('text/'):
            if encoding is None:
                encoding = self.encoding

            mimetype = f"{mimetype}; charset={encoding}"

        return mimetype

    def headers(self) -> Headers:
        headers = [('content-length', str(self.size)), ('content-type', self.mimetype)]

        headers.extend([('set-cookie', v) for v in self.cookie.values()])
        headers.extend([(k, v) for k, v in self.simple.items()])

        return headers


class Media(Http):
    __slots__ = 'file',

    def error(self, body: bytes, start_response: StartResponse) -> bytes:
        self.size = len(body)

        self.mimetype = self.iana('text/plain', 'ascii')

        start_response('500 Internal Server Error', self.headers())

        return body

    def __init__(self, file: str):
        super().__init__(self.iana(*mimetypes.guess_type(file, strict=True)))

        self.file = file

    def __call__(self, start_response: StartResponse) -> Generator[bytes, Any, None]:
        try:
            f = open(self.file, 'rb')

            self.size = os.path.getsize(self.file)

            start_response('200 OK', self.headers())

            for _ in range(0, self.size, self.block_size):
                yield f.read(self.block_size)

            f.close()

        except OSError:
            body = self.error(b'Error read file', start_response)

            for i in range(0, self.size, self.block_size):
                yield body[i:i + self.block_size]


class Document(Http):
    __slots__ = 'body', 'code'

    def __init__(
            self,
            body: bytes | str,
            *,
            code: int = 200,
            mimetype: str = 'text/plain',
            encoding: str = None,
    ):
        if encoding is None:
            encoding = self.encoding

        super().__init__(self.iana(mimetype, encoding))

        if isinstance(body, str):
            body = body.encode(encoding)

        self.size, self.body, self.code = len(body), body, code

    def status(self):
        return {
            200: '200 OK',
            307: '307 Temporary Redirect',
            308: '308 Permanent Redirect',
            404: '404 Not Found',
            500: '500 Internal Server Error',
        }[self.code]

    def __call__(self, start_response: StartResponse) -> Generator[bytes, None, None]:
        start_response(self.status(), self.headers())

        for i in range(0, self.size, self.block_size):
            yield self.body[i:i + self.block_size]
