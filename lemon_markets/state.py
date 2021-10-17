"""Module for showing the state of you account."""

from typing import List
from datetime import datetime

from lemon_markets.helpers.api_client import _ApiClient
from lemon_markets.helpers.time_helper import current_time
from lemon_markets.account import Account
from lemon_markets.space import Space


class State(_ApiClient):
    """
    Represents the state of an account.

    Parameters
    ----------
    account : Account
        The account with your space's credentials.
    cash_time_in_seconds : int
        Optional: The time requested data is cashed. Default is 10 seconds.

    Attributes
    ----------
    state : dict
        The state of the account.
    balance : float
        The balance of the account.
    spaces : list[Space]
        List of your spaces.

    Raises
    ------
    Exception
        Raised if theres an error with internal requests.

    """

    _state: dict = None
    _balance: float = None
    _spaces: List[Space] = None

    _latest_update: datetime = None
    _cash_storage_time: int = 10

    def __init__(self, account: Account, cash_time_in_seconds: int = 10):       # noqa
        super().__init__(account)
        self._cash_storage_time = cash_time_in_seconds
        self.get_state()
        self.get_spaces()
        self._latest_update = current_time()

    def get_state(self):
        """
        Get the state of a space.

        Raises
        ------
        Exception
            Raised if theres an internal request error

        """
        diff_since_last_update = self._latest_update - current_time()

        if diff_since_last_update.total_seconds() > self._cash_storage_time:
            data = self._request(endpoint='state/')
            try:
                self._balance = float(data.get('state').get('balance'))
                self._state = data
            except Exception:
                raise Exception

    def get_spaces(self):
        """Return a list of your spaces."""
        diff_since_last_update = self._latest_update - current_time()

        if diff_since_last_update.total_seconds() > self._cash_storage_time:
            data_rows = self._request_paged('spaces/')
            self._spaces = [Space._from_response(
                self._account, data) for data in data_rows]

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
    def balance(self) -> float:
        """
        Get the balance of the account.

        Returns
        -------
        float
            The balance of the account

        """
        self.get_state()
        return self._balance

    @property
    def state(self) -> dict:
        """
        Get the state of the account.

        Returns
        -------
        dict
            The state

        """
        self.get_state()
        return self._state

    @property
    def spaces(self) -> List[Space]:
        """
        Get the spaces of your account.

        Returns
        -------
        List of Spaces
            List of your spaces

        """
        self.get_spaces()
        return self._spaces
