from lemon_markets.helpers.requests import ApiRequest
from lemon_markets.config import DEFAULT_PAPER_REST_API_URL
from lemon_markets.helpers.api_object import ApiObject
from lemon_markets.account import Account


class Space(ApiObject):
    _url: str = None
    _account: Account

    class Values(ApiObject.Values):
        uuid: str = None
        name: str = None
        type: str = None
        state: dict = None

    def __init__(self, account: Account, uuid: str, name: str, type: str, state: dict):
        self._account = account
        self.Values.uuid = uuid
        self.Values.name = name
        self.Values.type = type
        self.Values.state = state

    def _update_url(self):
        self._url = DEFAULT_PAPER_REST_API_URL + "spaces/{" + self.Values.uuid + "}/"

    def _update_space_state(self):
        self._update_url()
        request = ApiRequest(url=self._url, method="GET", headers=self._account.authorization)
        self._update_values(request.response)

    @property
    def state(self):
        self._update_space_state()
        return self.Values.state

    @property
    def balance(self):
        self._update_space_state()
        return self.Values.state.get("balance")

    @property
    def cash_to_invest(self):
        self._update_space_state()
        return self.Values.state.get("cash_to_invest")


