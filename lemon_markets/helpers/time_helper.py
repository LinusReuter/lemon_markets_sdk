from datetime import datetime
from datetime import timedelta
from typing import Union


def timestamp_to_datetime(ts: Union[int, float]) -> datetime:
    return datetime.fromtimestamp(ts).astimezone()


def datetime_to_timestamp(dt: datetime) -> float:
    return dt.timestamp()


def current_time() -> datetime:  # gets time in local timezone
    return datetime.now().astimezone()


def time(year: int = datetime.now().year,
         month: int = datetime.now().month,
         day: int = datetime.now().day,
         hour: int = datetime.now().hour,
         minute: int = datetime.now().minute,
         second: int = datetime.now().second) -> datetime:  # gets time in local timezone
    return datetime(year=year,
                    month=month,
                    day=day,
                    hour=hour,
                    minute=minute,
                    second=second).astimezone()
