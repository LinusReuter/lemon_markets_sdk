from lemon_markets.helpers.requests import ApiRequest
from lemon_markets.config import DEFAULT_PAPER_REST_API_URL
from lemon_markets.helpers.api_object import ApiObject
from lemon_markets.account import Account


class State(ApiObject):
    _url = DEFAULT_PAPER_REST_API_URL + "state/"
    _account: Account

    class Values(ApiObject.Values):
        state: dict = None

    class BodyVariables(ApiObject.BodyVariables):
        limit: int
        offset: int

    def __init__(self, account: Account):
        self._account = account

    def request_state(self, limit: int = None, offset: int = None):
        self.BodyVariables.limit = limit
        self.BodyVariables.offset = offset
        body = self._build_body()
        request = ApiRequest(url=self._url, method="GET", body=body, headers=self._account.authorization)
        print(request.response)
        self._update_values(request.response)

    @property
    def get_balance(self, limit: int = None, offset: int = None):
        self.request_state(limit, offset)
        return self.Values.state.get("balance")


