from config import DEFAULT_AUTH_API_URL
from helpers.request import ApiRequest


class Account:
    _client_ID: str
    _client_secret: str

    _access_token: str
    _access_token_type: str
    _access_token_expires: int

    def __init__(self, client_ID, client_secret):
        self._client_ID = client_ID
        self._client_secret = client_secret

    def get_access_token(self):
        body = {"client_id": self._client_ID,
                "client_secret": self._client_secret,
                "grant_type": "client_credentials"}
        request = ApiRequest(url=DEFAULT_AUTH_API_URL, method="POST", body=body)
        print(request.response)
