import json
from json import JSONDecodeError
from typing import Union

import requests

from lemon_markets.helpers.errors import BaseError


class ApiResponseError(BaseError):

    def __init__(self, detail: str, status: int):
        try:
            self.status = status
            self.detail = json.loads(detail)
        except JSONDecodeError:
            self.detail = detail

    def to_representation(self):
        return "An error occurred while performing the request with error code {}: \n {}".format(self.status,
                                                                                                 str(self.detail))

class ApiResponse:
    content: dict = None
    status: int = 0
    _is_success: bool = True

    def __init__(self, content: Union[str, dict], status: int, is_success: bool, raise_error: bool = True):
        self.content = content
        self.status = status
        self._is_success = True
        if raise_error and not is_success:
            raise ApiResponseError(content, status)

    @property
    def successful(self):
        return self._is_success

    @property
    def has_errored(self):
        return not self._is_success


class ApiRequest:
    url: str
    method: str
    body: dict
    headers: dict
    url_params: dict = None
    _response: ApiResponse

    def __init__(self, url: str, method: str = "GET", body: dict = None, params: dict = None,
                 headers: dict = None):
        self.url = url
        self.method = method.lower()
        self.body = body
        self.headers = headers
        self.url_params = params

        self._perform_request()

    def _perform_request(self):
        try:
            if self.method == "post":
                response = requests.post(self.url, data=self.body)
            elif self.method == "delete":
                response = requests.delete(self.url, headers=self.headers, params=self.url_params)
            elif self.method == "patch":
                response = requests.patch(self.url, data=self.body, headers=self.headers, params=self.url_params)
            else:  # get
                response = requests.get(self.url, headers=self.headers, params=self.url_params)
            self._response = ApiResponse(content=response.content, status=response.status_code, is_success=response.ok)
        except Exception as e:
            raise e

    @property
    def response(self):
        if self._response.content:
            return json.loads(self._response.content)
        return self._response.content

