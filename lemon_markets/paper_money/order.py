from enum import Enum
from dataclasses import dataclass

from lemon_markets.helpers.api_client import ApiClient
from lemon_markets.account import Account
from lemon_markets.paper_money.instrument import Instrument, Instruments
from lemon_markets.paper_money.space import Space
from lemon_markets.helpers.time_helper import *


class OrderStatus(Enum):
    INACTIVE = 'inactive'
    ACTIVATED = 'activated'
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

    def update_data(self, data: dict):
        try:
            status_ = OrderStatus(data.get('status'))
        except (ValueError, KeyError):
            raise ValueError('Unexpected instrument type: %r' % data.get('type'))
        self.status = status_
        self.average_price = data.get('average_price')
        self.created_at = data.get('created_at')
        self.type = data.get('type')
        self.processed_at = data.get('processed_at')
        self.processed_quantity = data.get('processed_quantity')


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
        endpoint = f"spaces/{self._space.uuid}/orders/"
        data = {"isin": instrument.isin, "valid_until": datetime_to_timestamp(valid_until),
                  "side": side, "quantity": quantity}
        if stop_price is not None:
            data['stop_price'] = stop_price
        if limit_price is not None:
            data['limit_price'] = limit_price

        data = self._request(endpoint=endpoint, method="POST", data=data)
        order = Order.from_response(instrument, data)
        status = order.status
        self.orders[status.name].update({order.uuid: order})
        return order

    def update_order(self, order: Order):
        endpoint = f"spaces/{self._space.uuid}/orders/{order.uuid}/"
        old_status = order.status.name
        self.orders[old_status].pop(order.uuid)
        data = self._request(endpoint=endpoint, method="GET")
        order.update_data(data)
        new_status = order.status.name
        self.orders[new_status].update({order.uuid: order})
        status_changed = (old_status != new_status)
        return status_changed, new_status

    def activate_order(self, order: Order):
        endpoint = f"spaces/{self._space.uuid}/orders/{order.uuid}/activate/"
        old_status = order.status.name
        self.orders[old_status].pop(order.uuid)
        data = self._request(endpoint=endpoint, method="PUT")
        order.update_data(data)
        new_status = order.status.name
        self.orders[new_status].update({order.uuid: order})
        return new_status == 'ACTIVATED'

    def delete_order(self, order: Order):
        endpoint = f"spaces/{self._space.uuid}/orders/{order.uuid}/"
        self._request(endpoint=endpoint, method="DELETE")
        status_changed, new_status = self.update_order(order)
        return status_changed, new_status

    #requests all orders matching the paramerts and adds them to the orders dict
    def get_orders(self,
                   created_at_until: datetime = None,
                   created_at_from: datetime = None,
                   side: str = None,
                   type: str = None,
                   status: str = None):
        endpoint = f"spaces/{self._space.uuid}/orders/"
        params = {}
        if created_at_until is not None:
            params['created_at_until'] = datetime_to_timestamp(created_at_until)
        if created_at_from is not None:
            params['created_at_from'] = datetime_to_timestamp(created_at_from)
        if side is not None:
            params['side'] = side
        if type is not None:
            params['type'] = type
        if status is not None:
            params['status'] = status

        results = self._request_paged(endpoint=endpoint, params=params)

        #uuid's in old status
        inactive_uuids = list(self.orders['INACTIVE'])
        active_uuids = list(self.orders['ACTIVATED'])
        in_progress_uuids = list(self.orders['IN_PROGRESS'])
        executed_uuids = list(self.orders['EXECUTED'])
        deleted_uuids = list(self.orders['DELETED'])
        expired_uuids = list(self.orders['EXPIRED'])

        for o in results:
            uuid = o.get('uuid')
            if uuid in inactive_uuids:
                self.orders['INACTIVE'].pop(uuid)
            if uuid in active_uuids:
                self.orders['ACTIVATED'].pop(uuid)
            if uuid in in_progress_uuids:
                self.orders['IN_PROGRESS'].pop(uuid)
            if uuid in executed_uuids:
                self.orders['EXECUTED'].pop(uuid)
            if uuid in deleted_uuids:
                self.orders['DELETED'].pop(uuid)
            if uuid in expired_uuids:
                self.orders['EXPIRED'].pop(uuid)

            isin = o["instrument"].get("isin")
            instrument = Instruments(self._account).list_instruments(search=isin)[0]
            order = Order.from_response(instrument, o)
            self.orders[order.status.name].update({order.uuid: order})

    def clean_orders(self):  # removes all executed, deleted or expired orders in the orders dict
        executed_uuids = list(self.orders['EXECUTED'])
        deleted_uuids = list(self.orders['DELETED'])
        expired_uuids = list(self.orders['EXPIRED'])
        for uuid in executed_uuids:
            self.orders['EXECUTED'].pop(uuid)
        for uuid in deleted_uuids:
            self.orders['DELETED'].pop(uuid)
        for uuid in expired_uuids:
            self.orders['EXPIRED'].pop(uuid)
