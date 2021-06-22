import datetime
from enum import Enum
from dataclasses import dataclass

from lemon_markets.helpers.api_client import ApiClient
from lemon_markets.account import Account
from lemon_markets.paper_money.instrument import Instrument
from lemon_markets.paper_money.space import Space


class OrderStatus(Enum):
    INACTIVE = 'inactive'
    ACTIVE = 'active'
    IN_PROGRESS = 'in_progress'
    EXECUTED = 'executed'
    DELETED = 'deleted'
    EXPIRED = 'expired'


@dataclass()
class Order:
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
    trading_venue: dict = None

    @classmethod
    def from_response(cls, instrument: Instrument, data: dict):
        try:
            status_ = OrderStatus(data.get('status'))
        except (ValueError, KeyError):
            raise ValueError('Unexpected instrument type: %r' % data.get('type'))

        return cls(
            instrument=instrument,
            quantity=data.get('quantity'),
            valid_until=data.get('valid_until'),
            side=data.get('side'),
            stop_price=data.get('stop_price'),
            limit_price=data.get('limit_price'),
            uuid=data.get('uuid'),
            status=status_,
            trading_venue=data.get('trading_venue')
        )

    def activate(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass


class Orders(ApiClient):
    _space: Space
    orders = {}  # Structures all orders in a dict containing a list of orders for each last known order status.

    def __init__(self, account: Account, space: Space):
        self._space = space
        super().__init__(account=account)
        for status in OrderStatus:
            self.orders[status.name] = []

    def create_order(self):
        pass

    def update_order(self, order: Order):
        pass

    def activate_order(self, order: Order):
        pass

    def delete_order(self, order: Order):
        pass

    #requests all orders matching the paramerts and adds them to the orders dict
    def get_orders(self, created_at_until=None, created_at_from=None, side: str = None, type: str = None,
                   status: str = None):
        pass

    def clean_orders(self):  # remove all executed, deleted or expired orders in the orders dict
        pass
