from lemon_markets.helpers.api_client import ApiClient
from lemon_markets.account import Account

from enum import Enum
from dataclasses import dataclass
from typing import *


class InstrumentType(Enum):
    STOCKS = 'stocks'
    BONDS = 'bonds'
    FUNDS = 'fonds'
    WARRANTS = 'warrants'


@dataclass()
class Instrument:
    isin: str = None
    wkn: str = None
    title: str = None
    type: str = None
    symbol: str = None

    @classmethod
    def from_response(cls, data: dict):
        try:
            type_ = InstrumentType(data.get('type'))
        except (ValueError, KeyError):
            raise ValueError('Unexpected instrument type: %r' % data.get('type'))

        return cls(
            isin=data.get('isin'),
            wkn=data.get('wkn'),
            title=data.get('title'),
            type=type_,
            symbol=data.get('symbol'),
        )


class Instruments(ApiClient):

    def __init__(self, account: Account):
        super().__init__(account=account)

    def list_instruments(self, tradable: bool = None, search: str = None, currency: str = None, type_: InstrumentType = None) -> List[Instrument]:
        params = {}
        if tradable is not None:
            params['tradable'] = tradable
        if search is not None:
            params['search'] = search
        if currency is not None:
            params['currency'] = currency
        if type_ is not None:
            params['type'] = type_.value

        data_rows = self._request_paged('instruments/', params=params)
        return [Instrument.from_response(data) for data in data_rows]

    def get_instrument(self, isin: str) -> Instrument:
        data = self._request('instruments/'+isin+'/')
        return Instrument.from_response(data)
