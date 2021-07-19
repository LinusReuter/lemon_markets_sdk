from dataclasses import dataclass

from lemon_markets.helpers.api_client import ApiClient
from lemon_markets.account import Account

@dataclass()
class TradingVenue:
    name: str = None
    title: str = None
    mic: str = None
    opening_days: list = None



class TradingVenues(ApiClient):
    trading_venues = None

    def __init__(self, account: Account):
        super().__init__(account=account)
