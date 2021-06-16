from lemon_markets.helpers.requests import ApiRequest
from lemon_markets.config import DEFAULT_PAPER_REST_API_URL
from lemon_markets.helpers.api_object import ApiObject


class State(ApiObject):
    _url = DEFAULT_PAPER_REST_API_URL + "state/"

    class RespondVariables(ApiObject.RespondVariables):
        balance: float = None
        cash_to_invest: float = None

    class BodyVariables(ApiObject.BodyVariables):
        limit: int
        offset: int

    def __init__(self, authorization: dict, limit: int = None, offset: int = None):
        self.BodyVariables.limit = limit
        self.BodyVariables.offset = offset

        self.request_state(authorization)
        print(self.RespondVariables.balance)

    def request_state(self, authorization: dict, limit: int = None, offset: int = None):
        body = self._build_body()
        request = ApiRequest(url=self._url, method="GET", body=body, headers=authorization)
        self._set_data(request.response)




