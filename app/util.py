from datetime import date, datetime, timedelta
import isodate


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if isinstance(value, datetime) or isinstance(value, date):
        return value.isoformat()
    elif isinstance(value, timedelta):
        return isodate.duration_isoformat(value)

    raise TypeError("type not serializable")
