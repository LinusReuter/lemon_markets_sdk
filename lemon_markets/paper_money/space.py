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

    def __init__(self, account: Account, data: dict):
        self._account = account
        self._update_values(data)
        self._update_url()

    def _update_url(self):
        self._url = DEFAULT_PAPER_REST_API_URL + f"spaces/{self.Values.uuid}/"

    def _update_space_state(self):
        request = ApiRequest(url=self._url, method="GET", headers=self._account.authorization)
        self._update_values(request.response)

    @property
    def uuid(self):
        return self.Values.uuid

    @property
    def name(self):
        return self.Values.name

    @property
    def type(self):
        return self.Values.type

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


