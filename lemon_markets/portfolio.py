from dataclasses import dataclass

from lemon_markets.helpers.api_client import ApiClient
from lemon_markets.account import Account
from lemon_markets.instrument import Instrument, Instruments
from lemon_markets.space import Space


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


class Portfolio(ApiClient):
    _space: Space
    positions: list = []

    def __init__(self, account: Account, space: Space):
        self._space = space
        super().__init__(account=account)

    def update_positions(self):
        endpoint = f"spaces/{self._space.uuid}/portfolio/"
        data_rows = self._request_paged(endpoint=endpoint)

        self.positions = []
        for data in data_rows:
            isin = data["instrument"].get("isin")
            instrument = Instruments(self._account).list_instruments(search=isin)[0]
            self.positions.append(Position.from_response(instrument=instrument, data=data))
