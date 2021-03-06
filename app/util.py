import pendulum
import isodate
from urllib.parse import urljoin, urlparse
from werkzeug.routing import BaseConverter, ValidationError
import re
from flask import request
from wtforms import Field, widgets


def dateformat(d, format="%d/%m/%Y"):
    return d.strftime(format)


class DateConverter(BaseConverter):

    def to_python(self, value):
        try:
            date_of_night = pendulum.parse(value, exact=True)
        except Exception as e:
            raise ValidationError()
        # Forbid a date in the future
        if date_of_night > pendulum.today().date():
            raise ValidationError()
        return date_of_night

    def to_url(self, value):
        return value.strftime('%Y%m%d')


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if isinstance(value, pendulum.DateTime) or isinstance(value, pendulum.Date):
        return value.isoformat()
    elif isinstance(value, pendulum.Duration):
        return isodate.duration_isoformat(value)

    raise TypeError("type not serializable")


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


class TimeDeltaField(Field):
    widget = widgets.TextInput()

    def _value(self):
        if self.raw_data:
            return ' '.join(self.raw_data)
        else:
            return self.data and isodate.strftime(self.data, '%H:%M') or ''

    def process_formdata(self, valuelist):
        if valuelist:
            td_str = ' '.join(valuelist)
            try:
                h, m = re.split(':', td_str)
                self.data = pendulum.Duration(hours=int(h), minutes=int(m))
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid timedelta value'))
