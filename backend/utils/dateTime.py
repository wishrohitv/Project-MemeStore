from backend.modules import datetime, timezone


def datetimeUTC():
    return datetime.now(timezone.utc)
