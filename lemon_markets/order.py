"""Module for placing, listing and deleting orders."""

from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Union, Tuple

from lemon_markets.helpers.api_client import _ApiClient
from lemon_markets.account import Account
from lemon_markets.instrument import Instrument, Instruments, InstrumentType
from lemon_markets.space import Space
from lemon_markets.helpers.time_helper import timestamp_seconds_to_datetime, datetime_to_timestamp_seconds


class OrderStatus(Enum):
    """
    Class for different order statuses.

    Attributes
    ----------
    INACTIVE
        Order is inactive
    ACTIVATED
        Order is activated
    IN_PROGRESS
        Order is in in progress
    EXECUTED
        Order is done executed
    DELETED
        Order was deleted
    EXPIRED
        Order expired

    """

    INACTIVE = 'inactive'
    ACTIVATED = 'activated'
    IN_PROGRESS = 'in_progress'
    EXECUTED = 'executed'
    DELETED = 'deleted'
    EXPIRED = 'expired'


@dataclass()
class Order:
    """
    Dataclass representing an order.

    Attributes
    ----------
    instrument : Instrument
        The instrument that was ordered
    quantity : int
        The quantity
    valid_until : datetime
        The time until which the order is valid
    created_at : datetime
        The time it was created at
    processed_at : datetime
        The time the last part of the order was processed at
    processed_quantity : int
        The amount that is already processed (in case of partial processing)
    average_price : str
        The average price the order has been fulfilled at
    limit_price : float
        The limit price
    stop_price : float
        The stop price
    type : InstrumentType
        The type of the instrument
    side : str
        The side of the order. `buy` or `sell`
    uuid : str
        The order uuid
    status : OrderStatus
        The status of the order


    Raises
    ------
    ValueError
        Raised if the instrument type is unknown.

    """

    instrument: Instrument = None
    quantity: int = None
    valid_until: datetime = None
    created_at: datetime = None
    processed_at: datetime = None
    processed_quantity: int = None
    average_price: float = None
    limit_price: float = None
    stop_price: float = None
    type: str = None
    side: str = None
    uuid: str = None
    status: OrderStatus = None
    trading_venue: dict = None      # TODO convert to type TradingVenue

    @classmethod
    def _from_response(cls, instrument: Instrument, data: dict):

        try:
            status_ = OrderStatus(data.get('status'))
        except (ValueError, KeyError):
            raise ValueError('Unexpected instrument type: %r' %
                             data.get('type'))

        return cls(
            instrument=instrument,
            quantity=data.get('quantity'),
            valid_until=timestamp_seconds_to_datetime(data.get('valid_until')),
            side=data.get('side'),
            stop_price=data.get('stop_price'),
            limit_price=data.get('limit_price'),
            uuid=data.get('uuid'),
            status=status_,
            trading_venue=data.get('trading_venue')
        )

    def update_data(self, data: dict):
        """
        Update non-static properties from a request's data.

        Parameters
        ----------
        data : dict
            The request data

        Raises
        ------
        ValueError
            Raised if Instrumnt type is invalid

        """
        try:
            status_ = OrderStatus(data.get('status'))
        except (ValueError, KeyError):
            raise ValueError('Unexpected instrument type: %r' %
                             data.get('type'))
        self.status = status_
        self.average_price = data.get('average_price')
        self.created_at = data.get('created_at')
        self.type = InstrumentType(data.get('type'))
        self.processed_at = data.get('processed_at')
        self.processed_quantity = data.get('processed_quantity')


class Orders(_ApiClient):
    """
    Access orders for this space.

    Parameters
    ----------
    account : Account
        The account object
    space : Space
        The space object

    Attributes
    ----------
    orders : Mapping[str, Mapping[str, Order]]
        The orders. In a dict grouped by state and uuid.

    """

    _space: Space
    # Structures all orders in a dict containing a dict (the index is the uuid) of orders for each last known order status.
    orders = {}

    def __init__(self, account: Account, space: Space):     # noqa
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
                     limit_price: Union[int, float] = None) -> Order:
        """
        Create an order.

        Parameters
        ----------
        instrument : Instrument
            The instrument to buy/sell
        valid_until : datetime
            The time until which this order is valid
        side : str
            The side of the order. `buy` or `sell`
        quantity : int
            Quantity to order
        stop_price : Union[int, float], optional
            The price at which to activate the order
        limit_price : Union[int, float], optional
            The price limit while ordering

        Returns
        -------
        Order
            The order created

        """
        endpoint = f"spaces/{self._space.uuid}/orders/"
        data = {
            "isin": instrument.isin,
            "valid_until": datetime_to_timestamp_seconds(valid_until),
            "side": side, "quantity": quantity}
        if stop_price is not None:
            data['stop_price'] = stop_price
        if limit_price is not None:
            data['limit_price'] = limit_price

        data = self._request(endpoint=endpoint, method="POST", data=data)
        order = Order._from_response(instrument, data)
        status = order.status
        self.orders[status.name].update({order.uuid: order})
        return order

    def update_order(self, order: Order) -> Tuple[bool, OrderStatus]:
        """
        Update the order status.

        Parameters
        ----------
        order : Order
            The order to update

        Returns
        -------
        Union[bool, OrderStatus]
            status_changed:
                True if status has changed
            new_status:
                The new OrderStatus

        """
        old_status = self._update_oder_data(order, '/', "GET")
        new_status = OrderStatus(order.status.name)
        self.orders[new_status].update({order.uuid: order})
        status_changed = (old_status != new_status)
        return status_changed, new_status

    def activate_order(self, order: Order) -> bool:
        """
        Activate an order.

        Parameters
        ----------
        order : Order
            The order to update

        Returns
        -------
        bool
            `True` if the order was successfully activated

        """
        self._update_oder_data(order, '/activate/', "PUT")
        new_status = order.status.name
        self.orders[new_status].update({order.uuid: order})
        return new_status == 'ACTIVATED'

    def _update_oder_data(self, order, arg1, method):
        endpoint = f'spaces/{self._space.uuid}/orders/{order.uuid}{arg1}'
        result = order.status.name
        self.orders[result].pop(order.uuid)
        data = self._request(endpoint=endpoint, method=method)
        order.update_data(data)
        return result

    def delete_order(self, order: Order) -> Tuple[bool, OrderStatus]:
        """
        Delete specified order.

        Parameters
        ----------
        order : Order
            The order to delete

        Returns
        -------
        Tuple[bool, OrderStatus]
            Tuple in which the bool indicates success,
            and the OrderStatus is the new status of the order

        """
        endpoint = f"spaces/{self._space.uuid}/orders/{order.uuid}/"
        self._request(endpoint=endpoint, method="DELETE")
        status_changed, new_status = self.update_order(order)
        return status_changed, new_status

    # requests all orders matching the paramerts and adds them to the orders dict
    def fetch_orders(self,
                     created_at_until: datetime = None,
                     created_at_from: datetime = None,
                     side: str = None,
                     type: str = None,
                     status: str = None):
        """
        Return orders by criteria.

        Parameters
        ----------
        created_at_until : datetime, optional
            Limit results to orders created before this point in time
        created_at_from : datetime, optional
            Limit results to orders created after this point in time
        side : str, optional
            Filter by side. `buy` or `sell`
        type : str, optional
            Filter by type. `stock`, `bond`, `fund` or `warrant`
        status : str, optional
            Filter by status.

        """
        endpoint = f"spaces/{self._space.uuid}/orders/"
        params = {}
        if created_at_until is not None:
            params['created_at_until'] = datetime_to_timestamp_seconds(
                created_at_until)
        if created_at_from is not None:
            params['created_at_from'] = datetime_to_timestamp_seconds(created_at_from)
        if side is not None:
            params['side'] = side
        if type is not None:
            params['type'] = type
        if status is not None:
            params['status'] = status

        results = self._request_paged(endpoint=endpoint, params=params)

        # uuid's in old status
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
            instrument = Instruments(
                self._account).list_instruments(
                search=isin)[0]
            order = Order._from_response(instrument, o)
            self.orders[order.status.name].update({order.uuid: order})

    def clean_orders(self):
        """Remove executed, deleted and expired orders from the orders dict."""
        executed_uuids = list(self.orders['EXECUTED'])
        deleted_uuids = list(self.orders['DELETED'])
        expired_uuids = list(self.orders['EXPIRED'])
        for uuid in executed_uuids:
            self.orders['EXECUTED'].pop(uuid)
        for uuid in deleted_uuids:
            self.orders['DELETED'].pop(uuid)
        for uuid in expired_uuids:
            self.orders['EXPIRED'].pop(uuid)
