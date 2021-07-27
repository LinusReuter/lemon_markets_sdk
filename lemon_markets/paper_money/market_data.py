from dataclasses import dataclass
from datetime import datetime, timezone
import pandas as pd

from lemon_markets.helpers.api_client import ApiClient
from lemon_markets.account import Account
from lemon_markets.helpers.time_helper import datetime_to_timestamp
from lemon_markets.paper_money.instrument import Instrument
from lemon_markets.paper_money.trading_venue import TradingVenue


@dataclass()
class OHLC(ApiClient):

    def __init__(self, account: Account):
        super().__init__(account=account)

    def get_data(self, instrument: Instrument, venue: TradingVenue, x1: str, ordering: str = None,
                 date_from: datetime = None, date_until: datetime = None, as_df: bool = True):
        endpoint = f"trading-venues/{venue.mic}/instruments/{instrument.isin}/data/ohlc/{x1}/"
        params = {}
        if ordering is not None:
            params['ordering'] = ordering
        if date_from is not None:
            params['date_from'] = int(datetime_to_timestamp(date_from))
        if date_until is not None:
            params['date_until'] = int(datetime_to_timestamp(date_until))
        results = self._request(endpoint=endpoint, params=params)['results']

        if not as_df:
            return results
        else:
            from_tz = timezone.utc
            to_tz = datetime.now().astimezone().tzinfo
            print(from_tz, to_tz)
            df = pd.DataFrame(results)
            df['t'] = pd.to_datetime(df['t'], unit='s').dt.tz_localize(from_tz).dt.tz_convert(to_tz)
            df.set_index('t', inplace=True)
            if ordering == '-date':
                df.sort_index(ascending=False, inplace=True)
            else:
                df.sort_index(ascending=True, inplace=True)

            return df
