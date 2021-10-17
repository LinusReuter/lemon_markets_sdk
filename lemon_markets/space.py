"""Module for managing spaces."""

from lemon_markets.helpers.api_client import _ApiClient
from lemon_markets.account import Account
from lemon_markets.helpers.time_helper import current_time

from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class SpaceType(Enum):
    """
    Type of the space.

    Attributes
    ----------
    STRATEGY
        Type is `strategy`
    APP
        Type is `app`

    """

    STRATEGY = 'strategy'
    APP = 'app'


@dataclass
class Space(_ApiClient):
    """
    Class representing a space.

    Attributes
    ----------
    uuid : str
        The uuid of the space.
    name : str
        The name of the space.
    type : SpaceType
        The type of the space.
    state : dict
        The state of the space. The data gets automatically updated if it is older than 10 seconds. (Or your manually set cash time)
    balance : float
        The balance of the space. The data gets automatically updated if it is older than 10 seconds. (Or your manually set cash time)
    cash_to_invest : float
        The cash to invest. The data gets automatically updated if it is older than 10 seconds. (Or your manually set cash time)

    Raises
    ------
    ValueError
        If the space type is invalid

    """

    uuid: str = None
    name: str = None
    type: SpaceType = None
    _state: dict = None

    _account: Account = None

    _latest_update: datetime = None
    _cash_storage_time: int = 10

    @classmethod
    def _from_response(cls, account: Account, data: dict):
        try:
            type_ = SpaceType(data.get('type'))
        except (ValueError, KeyError):
            raise ValueError('Unexpected space type: %r' % data.get('type'))

        return cls(
            uuid=data.get('uuid'),
            name=data.get('name'),
            _state=data.get('state'),
            type=type_,
            _account=account,
            _latest_update=current_time()
        )

    def update_values(self, data: dict):
        """
        Update values from response data.

        Parameters
        ----------
        data : dict
            Response data

        Raises
        ------
        ValueError
            Raised if the space type in data is invalid

        """
        try:
            type_ = SpaceType(data.get('type'))
        except (ValueError, KeyError):
            raise ValueError('Unexpected space type: %r' % data.get('type'))

        self.uuid = data.get('uuid')
        self.name = data.get('name')
        self._state = data.get('state')
        self.type = type_

    def __post_init__(self):            # noqa
        super().__init__(account=self._account)

    def _update_space_state(self):
        diff_since_last_update = self._latest_update - current_time()

        if diff_since_last_update.total_seconds() > self._cash_storage_time:
            data = self._request(f"spaces/{self.uuid}/")
            self.update_values(data)

    # TODO revise docstring
    def change_cash_time(self, new_cash_time_in_seconds: int):
        """
        Change the time request results are cashed by multiple property calls.

        Parameters
        ----------
        new_cash_time_in_seconds : int
            The wished time data is cashed.

        """
        self._cash_storage_time = new_cash_time_in_seconds

    @property
    def state(self) -> dict:
        """
        Get the state of the space. The data gets automatically updated if it is older than 10 seconds.

        (Or your manually set cash time)

        Returns
        -------
        dict
            The space state

        """
        self._update_space_state()
        return self._state

    @property
    def balance(self) -> float:
        """
        Get space balance. The data gets automatically updated if it is older than 10 seconds.

        (Or your manually set cash time)

        Returns
        -------
        float
            The balance

        """
        self._update_space_state()
        return float(self._state.get("balance"))

    @property
    def cash_to_invest(self) -> float:
        """
        Get cash to invest. The data gets automatically updated if it is older than 10 seconds.

        (Or your manually set cash time)

        Returns
        -------
        float
            Cash to invest

        """
        self._update_space_state()
        return float(self._state.get("cash_to_invest"))
