from modules import datetime, timezone


def datetime_utc():
    return datetime.now(timezone.utc)
