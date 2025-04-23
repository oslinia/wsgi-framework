import re
from urllib.parse import unquote

from .. import Environment

env: Environment

query: "Query"
cookie: "Cookie"
form: "Form"


class Query(dict[str, str]):
    def __init__(self, environ: Environment):
        super().__init__()

        if e := environ['QUERY_STRING']:
            for key, value in (
                    ((v := q.split('=', 1))[0], '' if 1 == len(v) else v[1])
                    for q in unquote(e).split('&')
            ):
                self[key] = value


class Cookie(dict[str, str]):
    def __init__(self, environ: Environment):
        super().__init__()

        if 'HTTP_COOKIE' in environ:
            for key, value in (
                    ((p := i.split('='))[0], p[1])
                    for i in environ['HTTP_COOKIE'].split('; ')
            ):
                self[key] = value


class Form(object):
    __slots__ = '__boundary', 'data', 'upload'

    data: dict[str, str]
    upload: dict[str, dict[str, dict[str, str | bytes]]]

    def application(self, environ: Environment):
        if e := environ['wsgi.input'].read().decode('utf-8'):
            for key, value in (
                    ((p := i.split('=', 1))[0], p[1] if 1 < len(p) else '')
                    for i in e.split('&')
            ):
                self.data[key] = value

    def multipart(self, environ: Environment):
        i, d, name, filename, not_empty = 0, -1, None, None, False

        for line in environ['wsgi.input'].readlines():
            if self.__boundary in line:
                if name is not None:
                    if name in self.data.keys():
                        self.data[name] = re.sub(r'\r\n$', '', self.data[name])

                    elif name in self.upload.keys():
                        file = self.upload[name].get(filename)

                        if file is not None:
                            self.upload[name][filename]['body'] = re.sub(b'\\r\\n$', b'', file['body'])

                d, name, filename, not_empty = i + 1, None, None, False

            if i == d:
                if line.startswith(b'Content-Disposition'):
                    d, items = i + 1, re.sub(b'\\r\\n$', b'', line).split(b'; ')[1:]

                    if 1 == len(items):
                        name = items[0].decode('ascii').split('=')[1].strip('"')

                        self.data[name] = ''

                    else:
                        for item in items:
                            key, value = (s := item.decode('ascii').split('='))[0], s[1].strip('"')

                            match key:
                                case 'name':
                                    name = value

                                    if name not in self.upload.keys():
                                        self.upload[name] = dict()

                                case 'filename':
                                    filename, not_empty = value, '' != value

                                    if not_empty:
                                        self.upload[name][filename] = {'type': None, 'body': b''}

                if line.startswith(b'Content-Type'):
                    d, line = i + 1, re.sub(b'\\r\\n$', b'', line)

                    if filename in self.upload[name].keys():
                        self.upload[name][filename]['type'] = line.decode('ascii').split(': ')[1]

            elif name is not None:
                if filename is None:
                    self.data[name] += line.decode('utf-8')

                elif not_empty:
                    self.upload[name][filename]['body'] += line

            i += 1

    def __init__(self, environ: Environment):
        self.data = dict()
        self.upload = dict()

        if 'CONTENT_TYPE' in environ:
            content = environ['CONTENT_TYPE'].split('; ')

            if hasattr(self, method := content[0].split('/')[0]):
                if 2 == len(content):
                    self.__boundary: str = content[1].split('=')[1].encode('ascii')

                getattr(self, method)(environ)
