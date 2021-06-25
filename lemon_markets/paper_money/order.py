from datetime import datetime
from enum import Enum
from dataclasses import dataclass
from typing import *

from lemon_markets.helpers.api_client import ApiClient
from lemon_markets.account import Account
from lemon_markets.paper_money.instrument import Instrument
from lemon_markets.paper_money.space import Space
from lemon_markets.helpers.time_helper import *


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
    valid_until: datetime = None
    created_at: datetime = None
    processed_at: datetime = None
    processed_quantity: int = None
    average_price: str = None
    limit_price: float = None
    stop_price: float = None
    type: str = None
    side: str = None
    uuid: str = None
    status: OrderStatus = None
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
            valid_until=timestamp_to_datetime(data.get('valid_until')),
            side=data.get('side'),
            stop_price=data.get('stop_price'),
            limit_price=data.get('limit_price'),
            uuid=data.get('uuid'),
            status=status_,
            trading_venue=data.get('trading_venue')
        )

    def activate(self):
        pass

    def update(self, data: dict):
        pass

    def delete(self):
        pass


class Orders(ApiClient):
    _space: Space
    orders = {}  # Structures all orders in a dict containing a dict (the index is the uuid) of orders for each last known order status.

    def __init__(self, account: Account, space: Space):
        self._space = space
        super().__init__(account=account)
        for status in OrderStatus:
            self.orders[status.name] = {}

    def create_order(self,
                     instrument: Instrument,
                     valid_until: datetime,
                     side: str,
                     quantity: int,
                     stop_price: Union[int, float] = None,
                     limit_price: Union[int, float] = None):
        endpoint = f"/spaces/{self._space.uuid}/orders/"
        params = {"isin": instrument.isin, "valid_until": datetime_to_timestamp(valid_until),
                  "side": side, "quantity": quantity}
        if stop_price is not None:
            params['stop_price'] = stop_price
        if limit_price is not None:
            params['limit_price'] = limit_price

        data = self._request(endpoint=endpoint, method="POST", params=params)
        order = Order.from_response(instrument, data)
        status = order.status
        self.orders[status].update({order.uuid: order})
        pass

    def update_order(self, order: Order):
        endpoint = f"/spaces/{self._space.uuid}/orders/{order.uuid}/"
        old_status = order.status
        self.orders[old_status].pop(order.uuid)
        data = self._request(endpoint=endpoint, method="GET")
        order.update(data)
        new_status = order.status
        self.orders[new_status].update({order.uuid: order})
        status_changed = (old_status != new_status)
        return status_changed, new_status

    def activate_order(self, order: Order):
        pass

    def delete_order(self, order: Order):
        pass

    #requests all orders matching the paramerts and adds them to the orders dict
    def get_orders(self,
                   created_at_until: datetime = None,
                   created_at_from: datetime = None,
                   side: str = None,
                   type: str = None,
                   status: str = None):
        pass

    def clean_orders(self):  # remove all executed, deleted or expired orders in the orders dict
        pass
