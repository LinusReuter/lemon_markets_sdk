from datetime import datetime
from typing import Union


def timestamp_to_datetime(ts: Union[int, float]) -> datetime:
    return datetime.fromtimestamp(ts).astimezone()


def datetime_to_timestamp(dt: datetime) -> float:
    return dt.timestamp()
    pass


def current_time() -> datetime:  # gets time in local timezone
    return datetime.now().astimezone()
