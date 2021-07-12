import time
import requests
import json

from lemon_markets.config import DEFAULT_AUTH_API_URL
from lemon_markets.exceptions import LemonConnectionException


class Account:
    _client_ID: str
    _client_secret: str

    _access_token: str
    _access_token_type: str
    _access_token_expires: int

    def __init__(self, client_id, client_secret):
        self._client_ID = client_id
        self._client_secret = client_secret
        self.request_access_token()

    def request_access_token(self):
        data = {"client_id": self._client_ID,
                "client_secret": self._client_secret,
                "grant_type": "client_credentials"}
        response = requests.post(url=DEFAULT_AUTH_API_URL, data=data)
        response.raise_for_status()

        data = json.loads(response.content)

        self._access_token = data.get("access_token")
        self._access_token_type = data.get("token_type")
        self._access_token_expires = int(time.time()) + data.get("expires_in") - 60

    @property
    def access_token(self):
        if time.time() > self._access_token_expires:
            self.request_access_token()

        return self._access_token

    @property
    def access_token_type(self):
        if time.time() > self._access_token_expires:
            self.request_access_token()

        return self._access_token_type

    @property
    def authorization(self):
        if self._access_token_type == "bearer":
            s = "Bearer " + self.access_token
        else:
            raise LemonConnectionException("Error: unknown token type")

        return {"Authorization": s}
