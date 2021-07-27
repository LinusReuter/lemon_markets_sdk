import json
import requests
from typing import *

from lemon_markets.account import Account
from lemon_markets.config import DEFAULT_PAPER_REST_API_URL
from lemon_markets.exceptions import LemonConnectionException, LemonAPIException


class ApiClient:

    def __init__(self, account: Account = None, endpoint: str = None):
        self._account = account
        self._endpoint = endpoint or DEFAULT_PAPER_REST_API_URL

    def _request_paged(self, endpoint, data_=None, params=None) -> List[dict]:

        # Keep requesting until there are no more pages
        next = None
        results = []

        try:

            while True:

                if next is not None:
                    data = self._request(next, data=data_, url_prefix=False)
                else:
                    data = self._request(endpoint, data=data_, params=params)

                results += data['results']

                if data['next'] is None or data['next'] == next:
                    break
                else:
                    next = data['next']
        except requests.Timeout:
            raise LemonConnectionException("Network Timeout on url: %s" % endpoint)

        return results

    def _request(self, endpoint, method='GET', data=None, params=None, url_prefix=True):
        method = method.lower()
        if url_prefix:
            url = self._endpoint+endpoint
        else:
            url = endpoint
        headers = self._account.authorization

        try:
            if method == 'get':
                response = requests.get(url=url, params=params, headers=headers)
            elif method == 'post':
                response = requests.post(url=url, data=data, params=params, headers=headers)
            elif method == 'put':
                response = requests.put(url=url, headers=headers)
            elif method == 'patch':
                response = requests.patch(url=url, data=data, params=params, headers=headers)
            elif method == 'delete':
                response = requests.delete(url=url, params=params, headers=headers)
            else:
                raise ValueError('Unknown method: %r' % method)

            response.raise_for_status()

        except requests.Timeout:
            raise LemonConnectionException("Network Timeout on url: %s" % url)

        if response.status_code > 399:
            raise LemonAPIException(status=response.status_code, errormessage=response.reason)

        if method != 'delete':
            data = json.loads(response.content)
        return data
