from .call import env, media, Query, Cookie, Form
from .head import header, has, delete, cookies
from .routing import Link
from .template import Template

link: Link

dirname: str
static_urlpath: str

query: Query
cookie: Cookie
form: Form

encoding: str | None
