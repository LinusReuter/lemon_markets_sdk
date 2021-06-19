import datetime
from typing import Union

from lemon_markets.helpers.requests import ApiRequest
from lemon_markets.config import DEFAULT_PAPER_REST_API_URL
from lemon_markets.helpers.api_object import ApiObject
from lemon_markets.account import Account
from lemon_markets.paper_money.instrument import Instrument


class Order(ApiObject):
    _url = DEFAULT_PAPER_REST_API_URL + "orders/"

    class Values(ApiObject.Values):
        account: Account = None
        instrument: Instrument = None
        quantity: int = None
        valid_until: datetime.datetime = None
        created_at: datetime.datetime = None
        processed_at: datetime.datetime = None
        processed_quantity: int = None
        average_price: str = None
        limit_price: float = None
        stop_price: float = None
        type: str = None
        side: str = None
        uuid: str = None
        status: str = None

    def __init__(self,
                 account: Account = None,
                 instrument: Instrument = None,
                 quantity: int = None,
                 valid_until: Union[float, int, datetime.datetime] = None,
                 limit_price: float = None,
                 stop_price: float = None,
                 type: str = None,
                 side: str = None,
                 uuid: str = None,
                 ):
        self._update_values(locals())

    @property
    def instrument(self):
        return self.Values.instrument

    @property
    def quantity(self):
        return self.Values.quantity

    @property
    def valid_until(self):
        return self.Values.valid_until

    @property
    def created_at(self):
        return self.Values.created_at

    @property
    def processed_at(self):
        return self.Values.processed_at

    @property
    def processed_quantity(self):
        return self.Values.processed_quantity

    @property
    def average_price(self):
        return self.Values.average_price

    @property
    def limit_price(self):
        return self.Values.limit_price

    @property
    def stop_price(self):
        return self.Values.stop_price

    @property
    def type(self):
        return self.Values.type

    @property
    def side(self):
        return self.Values.side

    @property
    def uuid(self):
        return self.Values.uuid

    @property
    def status(self):
        return self.Values.status
