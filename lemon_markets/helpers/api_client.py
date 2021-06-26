import json
import requests
from typing import *

from lemon_markets.account import Account
from lemon_markets.config import DEFAULT_PAPER_REST_API_URL


class ApiClient:

    def __init__(self, account: Account = None, endpoint: str = None):
        self._account = account
        self._endpoint = endpoint or DEFAULT_PAPER_REST_API_URL

    def _request_paged(self, endpoint, data_=None, params=None) -> List[dict]:
        if params is None:
            params = {}

        # Keep requesting until there are no more pages
        offset = None
        next = None
        results = []
        while True:
            offset = next
            page_params = params.copy()
            if offset is not None:
                page_params['offset'] = offset
            data = self._request(endpoint, data=data_, params=page_params)

            results += data['results']

            if data['next'] is None or data['next'] <= offset:
                break
            else:
                next = data['next']

        return results

    def _request(self, endpoint, method='GET', data=None, params=None):
        method = method.lower()
        url = self._endpoint+endpoint
        headers = self._account.authorization

        if method == 'get':
            response = requests.get(url=url, params=params, headers=headers)
        elif method == 'post':
            response = requests.post(url=url, data=data, headers=headers)
        elif method == 'put':
            response = requests.put(url=url, headers=headers)
        elif method == 'patch':
            response = requests.patch(url=url, data=data, params=params, headers=headers)
        elif method == 'delete':
            response = requests.delete(url=url, params=params, headers=headers)
        else:
            raise ValueError('Unknown method: %r' % method)

        response.raise_for_status()

        if method != 'delete':
            data = json.loads(response.content)
        return data
