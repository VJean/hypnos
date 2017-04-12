from datetime import date, datetime, timedelta
import isodate
from urllib.parse import urljoin, urlparse
from flask import request


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if isinstance(value, datetime) or isinstance(value, date):
        return value.isoformat()
    elif isinstance(value, timedelta):
        return isodate.duration_isoformat(value)

    raise TypeError("type not serializable")


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
