from lemon_markets.helpers.api_client import ApiClient
from lemon_markets.account import Account

from enum import Enum
from dataclasses import dataclass


class SpaceType(Enum):
    STRATEGY = 'strategy'
    APP = 'app'


@dataclass
class Space(ApiClient):
    uuid: str = None
    name: str = None
    type: str = None
    _state: dict = None

    _account: Account = None

    @classmethod
    def from_response(cls, account: Account, data: dict):
        try:
            type_ = SpaceType(data.get('type'))
        except (ValueError, KeyError):
            raise ValueError('Unexpected space type: %r' % data.get('type'))

        return cls(
            uuid=data.get('uuid'),
            name=data.get('name'),
            _state=data.get('state'),
            type=type_,
            _account=account
        )

    def update_values(self, data: dict):
        try:
            type_ = SpaceType(data.get('type'))
        except (ValueError, KeyError):
            raise ValueError('Unexpected space type: %r' % data.get('type'))

        self.uuid = data.get('uuid')
        self.name = data.get('name')
        self._state = data.get('state')
        self.type = type_

    def __post_init__(self):
        super().__init__(account=self._account)

    def _update_space_state(self):
        data = self._request(f"spaces/{self.uuid}/")
        self.update_values(data)

    @property
    def state(self):
        self._update_space_state()
        return self._state

    @property
    def balance(self):
        self._update_space_state()
        return float(self._state.get("balance"))

    @property
    def cash_to_invest(self):
        self._update_space_state()
        return float(self._state.get("cash_to_invest"))
