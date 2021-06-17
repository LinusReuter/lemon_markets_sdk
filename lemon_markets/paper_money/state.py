from lemon_markets.helpers.requests import ApiRequest
from lemon_markets.config import DEFAULT_PAPER_REST_API_URL
from lemon_markets.helpers.api_object import ApiObject
from lemon_markets.account import Account
from lemon_markets.paper_money.space import Space


class State(ApiObject):
    _url_state = DEFAULT_PAPER_REST_API_URL + "state/"
    _url_spaces = DEFAULT_PAPER_REST_API_URL + "spaces/"
    _account: Account

    class Values(ApiObject.Values):
        state: dict = None
        spaces: [Space] = []

    class ParamVariables(ApiObject.ParamVariables):
        limit: int
        offset: int

    def __init__(self, account: Account):
        self._account = account

    def request(self, type_of_request: str, limit: int = None, offset: int = None):
        self.ParamVariables.limit = limit
        self.ParamVariables.offset = offset
        params = self._build_params()
        if type_of_request == "state":
            url = self._url_state
        else:
            url = self._url_spaces
        request = ApiRequest(url=url, method="GET", params=params, headers=self._account.authorization)
        if type_of_request == "state":
            self._update_values(request.response)
        else:
            self.Values.spaces = []
            results = request.response["results"]
            for s in results:
                self.Values.spaces.append(Space(self._account, s))

    @property
    def state(self, limit: int = None, offset: int = None):
        self.request("state", limit, offset)
        return self.Values.state

    @property
    def balance(self, limit: int = None, offset: int = None):
        self.request("state", limit, offset)
        return self.Values.state.get("balance")

    @property
    def spaces(self, limit: int = None, offset: int = None):
        self.request("spaces", limit, offset)
        return self.Values.spaces



