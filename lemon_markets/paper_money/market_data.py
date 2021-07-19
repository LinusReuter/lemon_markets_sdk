from dataclasses import dataclass
from datetime import datetime

from lemon_markets.helpers.api_client import ApiClient
from lemon_markets.account import Account
from lemon_markets.helpers.time_helper import datetime_to_timestamp
from lemon_markets.paper_money.instrument import Instrument
from lemon_markets.paper_money.trading_venue import TradingVenue


@dataclass()
class OHLC(ApiClient):

    def __init__(self, account: Account):
        super().__init__(account=account)

    def get_data(self, instrument: Instrument, venue: TradingVenue, X1: str, ordering: str = None,
                 date_from: datetime = None, date_until: datetime = None):
        endpoint = f"trading-venues/{TradingVenue.mic}/instruments/{Instrument.isin}/data/ohlc/{X1}/"
        params = {}
        if ordering is not None:
            params['ordering'] = ordering
        if date_from is not None:
            params['date_from'] = int(datetime_to_timestamp(date_from))
        if date_until is not None:
            params['date_until'] = int(datetime_to_timestamp(date_until))
        return self._request_paged(endpoint=endpoint, params=params)
