"""Various helper functions for dealing with time."""
from datetime import datetime
from typing import Union


def timestamp_seconds_to_datetime(ts: Union[int, float]) -> datetime:
    """
    Convert unix timestamp to datetime object.

    Parameters
    ----------
    ts : Union[int, float]
        The timestamp to convert

    Returns
    -------
    datetime
        The corresponding datetime object

    """
    return datetime.fromtimestamp(ts).astimezone()


def datetime_to_timestamp_seconds(dt: datetime) -> float:
    """
    Convert datetime to unix timestamp.

    Parameters
    ----------
    dt : datetime
        The datetime object

    Returns
    -------
    float
        The unix timestamp

    """
    return int(dt.timestamp())


def timestamp_milliseconds_to_datetime(ts: Union[int, float]) -> datetime:
    """
    Convert unix milliseconds timestamp to datetime object.

    Parameters
    ----------
    ts : Union[int, float]
        The timestamp in milliseconds to convert

    Returns
    -------
    datetime
        The corresponding datetime object

    """
    return datetime.fromtimestamp(ts / 1000).astimezone()


def datetime_to_timestamp_milliseconds(dt: datetime) -> float:
    """
    Convert datetime to unix milliseconds timestamp.

    Parameters
    ----------
    dt : datetime
        The datetime object

    Returns
    -------
    float
        The unix milliseconds timestamp

    """
    return int(dt.timestamp() * 1000)


def current_time() -> datetime:  # gets time in local timezone
    """Return timezone-aware current time as datetime."""
    return datetime.now().astimezone()


def time(year: int = datetime.now().year,
         month: int = datetime.now().month,
         day: int = datetime.now().day,
         hour: int = datetime.now().hour,
         minute: int = datetime.now().minute,
         second: int = datetime.now().second) -> datetime:  # gets time in local timezone
    """Return the current datetime in local timezone."""
    return datetime(year=year,
                    month=month,
                    day=day,
                    hour=hour,
                    minute=minute,
                    second=second).astimezone()
