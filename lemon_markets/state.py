from lemon_markets.helpers.api_client import ApiClient
from lemon_markets.account import Account
from lemon_markets.space import Space


class State(ApiClient):
    _state: dict = None
    _balance: float = None
    _spaces: [Space] = None

    def __init__(self, account: Account):
        super().__init__(account)

    def get_state(self):
        data = self._request(endpoint='state/')
        try:
            self._balance = float(data.get('balance'))
            self._state = data
        except Exception:
            raise Exception

    def get_spaces(self):
        data_rows = self._request_paged('spaces/')
        self._spaces = [Space.from_response(self._account, data) for data in data_rows]

    @property
    def balance(self):
        self.get_state()
        return self._balance

    @property
    def state(self):
        self.get_state()
        return self._state

    @property
    def spaces(self):
        self.get_spaces()
        return self._spaces
