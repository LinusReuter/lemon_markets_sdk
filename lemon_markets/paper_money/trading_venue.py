from dataclasses import dataclass

from lemon_markets.helpers.api_client import ApiClient
from lemon_markets.account import Account

@dataclass()
class TradingVenue:
    name: str = None
    title: str = None
    mic: str = None
    opening_days: list = None
    request_class: object = None

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
        return None

    @property
    def time_until_close(self):
        return None

    @property
    def time_until_open(self):
        return None


class TradingVenues(ApiClient):
    trading_venues = None

    def __init__(self, account: Account):
        super().__init__(account=account)

    def get_venues(self):
        data_rows = self._request_paged('trading-venues/')
        self.trading_venues = [TradingVenue.from_response(self, data) for data in data_rows]

    def get_opening_days(self, mic):
        return self._request(endpoint=f"trading-venues/{mic}/opening-days")

