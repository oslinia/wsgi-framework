import re
from datetime import datetime, timezone


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
