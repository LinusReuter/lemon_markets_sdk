from enum import Enum
from dataclasses import dataclass

from lemon_markets.helpers.api_client import ApiClient
from lemon_markets.account import Account
from lemon_markets.paper_money.instrument import Instrument, Instruments
from lemon_markets.paper_money.space import Space
from lemon_markets.helpers.time_helper import *


@dataclass()
class Position:
    instrument: Instrument = None
    quantity: int = None
    average_price: float = None
    latest_total_value: float = None

    @classmethod
    def from_response(cls, instrument: Instrument, data: dict):

        return cls(
            instrument=instrument,
            quantity=data.get('quantity'),
            average_price=data.get('average_price'),
            latest_total_value=data.get('latest_total_value')
        )
