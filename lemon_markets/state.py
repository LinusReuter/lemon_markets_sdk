from typing import List

from lemon_markets.helpers.api_client import _ApiClient
from lemon_markets.account import Account
from lemon_markets.space import Space


class State(_ApiClient):
    """
    Represents the state of an account.

    Raises
    ------
    Exception
        Raised if theres an error with internal requests.

    """

    _state: dict = None
    _balance: float = None
    _spaces: List[Space] = None

    def __init__(self, account: Account):
        """
        Initialise using the account.

        Parameters
        ----------
        account : Account
            The account with your space's credentials.

        """
        super().__init__(account)

    def get_state(self):
        """
        Get the state of a space.

        Raises
        ------
        Exception
            Raised if theres an internal request error

        """
        data = self._request(endpoint='state/')
        try:
            self._balance = float(data.get('state').get('balance'))
            self._state = data
        except Exception:
            raise Exception

    def get_spaces(self):
        """Return a list of your spaces."""
        data_rows = self._request_paged('spaces/')
        self._spaces = [Space.from_response(
            self._account, data) for data in data_rows]

    @property
    def balance(self) -> float:
        """
        Get the balance of a space.

        Returns
        -------
        float
            The balance of the space

        """
        self.get_state()
        return self._balance

    @property
    def state(self) -> dict:
        """
        Get the state of the space.

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
