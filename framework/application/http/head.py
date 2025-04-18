import re
from datetime import datetime, timezone, timedelta
from typing import Literal

from .call.response import Head
from ...http import utc


def header(name: str, value: str):
    Head.simple[name] = value


def has(name: str):
    return name in Head.simple


def delete(name: str):
    if has(name):
        del Head.simple[name]


def format_expires(variable: datetime | float | int | str):
    wd = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
    mn = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

    if isinstance(variable, float | int):
        variable = datetime.fromtimestamp(variable, tz=timezone.utc)

    if isinstance(variable, datetime):
        if variable.tzinfo is None or variable.tzinfo != timezone.utc:
            raise ValueError('Cookie requires UTC datetime.')

        t = variable.timetuple()

        return '%s, %02d %s %04d %02d:%02d:%02d GMT' % (wd[t[6]], t[2], mn[t[1] - 1], t[0], t[3], t[4], t[5])

    else:
        if r := re.search(r'^([A-Za-z]{3}), (\d{2}) ([A-Za-z]{3}) (\d{4}) (\d{2}:\d{2}:\d{2}) GMT$', variable):
            if r[1] in wd and r[3] in mn:
                return variable

        raise ValueError('Datetime string format does not match for cookie.')


def expires_max_age(expires: datetime | float | int | str | None, max_age: timedelta | int | None):
    if expires is None:
        body = ''

    else:
        body = f"; expires={format_expires(expires)}"

    if max_age is not None:
        if isinstance(max_age, timedelta):
            max_age = int(max_age.total_seconds())

        if '' == body:
            body = f"; expires={format_expires(utc.timestamp + max_age)}"

        return f"{body}; Max-Age={max_age}"

    return body


def security(httponly: bool, secure: bool, samesite: str | None):
    body = ''

    if httponly:
        body = '; HttpOnly'

    if secure:
        body = f"{body}; Secure"

    if samesite is not None and samesite in ('Lax', 'None', 'Strict'):
        return f"{body}; SameSite={samesite}"

    return body


def cookies(
        name: str,
        value: str | None,
        domain: str | None,
        path: str,
        expires: datetime | float | int | str | None,
        max_age: timedelta | int | None,
        httponly: bool,
        secure: bool,
        samesite: Literal['Lax', 'None', 'Strict'] | None,
):
    if value is None:
        value = ''

    body = f"{name}={value}{expires_max_age(expires, max_age)}"

    if domain is not None:
        body = f"{body}; Domain={domain}"

    Head.cookie[name] = f"{body}; Path={path}{security(httponly, secure, samesite)}"
