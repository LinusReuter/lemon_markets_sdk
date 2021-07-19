from dataclasses import dataclass

from lemon_markets.helpers.api_client import ApiClient
from lemon_markets.account import Account
from lemon_markets.helpers.time_helper import *


class TradingVenues(ApiClient):
    trading_venues = None

    def __init__(self, account: Account):
        super().__init__(account=account)

    def get_venues(self):
        data_rows = self._request_paged('trading-venues/')
        self.trading_venues = [TradingVenue.from_response(self, data) for data in data_rows]

    def get_opening_days(self, mic):
        return self._request(endpoint=f"trading-venues/{mic}/opening-days")


@dataclass()
class TradingVenue:
    name: str = None
    title: str = None
    mic: str = None
    opening_days: list = None
    request_class: TradingVenues = None

    @classmethod
    def from_response(cls, request_class, data: dict):

        return cls(
            request_class=request_class,
            name=data.get('name'),
            title=data.get('title'),
            mic=data.get('mic')
        )

    @property
    def is_open(self):
        day = current_time().strftime("%Y-%m-%d")
        if self.opening_days is None:
            self.get_opening_days()

        for data in self.opening_days:
            if day == data.get('day_iso'):
                if timestamp_to_datetime(data.get("opening_time")) <= current_time() <= timestamp_to_datetime(
                        data.get("closing_time")):
                    return True
                else:
                    return False

        self.get_opening_days()
        for data in self.opening_days:
            if day == data.get('day_iso'):
                if timestamp_to_datetime(data.get("opening_time")) <= current_time() <= timestamp_to_datetime(
                        data.get("closing_time")):
                    return True
                else:
                    return False

        return False

    @property
    def time_until_close(self):
        day = current_time().strftime("%Y-%m-%d")
        if self.opening_days is None:
            self.get_opening_days()

        for data in self.opening_days:
            if day == data.get('day_iso'):
                return timestamp_to_datetime(data.get("closing_time")) - current_time()

        self.get_opening_days()
        for data in self.opening_days:
            if day == data.get('day_iso'):
                return timestamp_to_datetime(data.get("closing_time")) - current_time()

        return timedelta()

    @property
    def time_until_open(self):
        day = current_time().strftime("%Y-%m-%d")
        if self.opening_days is None:
            self.get_opening_days()

        for data in self.opening_days:
            if day == data.get('day_iso'):
                return timestamp_to_datetime(data.get("opening_time")) - current_time()

        self.get_opening_days()
        for data in self.opening_days:
            if day == data.get('day_iso'):
                return timestamp_to_datetime(data.get("opening_time")) - current_time()

        return timedelta()

    def get_opening_days(self):
        self.opening_days = self.request_class.get_opening_days(self.mic)
