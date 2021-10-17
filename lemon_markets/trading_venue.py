"""Module for listing trading venues and their opening/closing times."""

from dataclasses import dataclass
from datetime import timedelta

from lemon_markets.helpers.api_client import _ApiClient
from lemon_markets.account import Account
from lemon_markets.helpers.time_helper import current_time, timestamp_seconds_to_datetime


class TradingVenues(_ApiClient):
    """
    Available trading venues.

    Attributes
    ----------
    trading_venues : list[TradingVenue]
        A list of all Trading venues.

    Parameters
    ----------
    account : Account
        Your auth data

    """

    trading_venues = None
    _account = None

    def __init__(self, account: Account):       # noqa
        _account = account
        super().__init__(account=_account, is_data=True)

    def get_venues(self):
        """Load the list of trading venues."""
        data = self._request(endpoint='venues/')
        data_rows = data.get("results")
        self.trading_venues = [TradingVenue._from_response(
            self._account, data) for data in data_rows]


@dataclass()
class TradingVenue(_ApiClient):  # TODO update openig checks for new AIP Strcture
    """A trading venue."""

    name: str = None
    title: str = None
    mic: str = None
    currency: str = None
    opening_days: list = None
    opening_time = None
    closing_time = None
    _account: Account = None

    @classmethod
    def _from_response(cls, account, data: dict):
        return cls(
            _account=account,
            name=data.get('name'),
            title=data.get('title'),
            mic=data.get('mic'),
            currency=data.get("currency"),
            opening_days=data.get('opening_days')
        )

    def __post_init__(self):            # noqa
        super().__init__(self._account, is_data=True)

    @property
    def is_open(self) -> bool:
        """
        Check if the venue is open.

        Returns
        -------
        bool
            True if the venue is open, False otherwise

        """
        day = current_time().strftime("%Y-%m-%d")
        if self.opening_days is None:
            self.update_opening_days()

        for data in self.opening_days:
            if day == data.get('day_iso'):
                return (
                    timestamp_seconds_to_datetime(data.get("opening_time"))
                    <= current_time()
                    <= timestamp_seconds_to_datetime(data.get("closing_time"))
                )

        self.update_opening_days()
        for data in self.opening_days:
            if day == data.get('day_iso'):
                return (
                    timestamp_seconds_to_datetime(data.get("opening_time"))
                    <= current_time()
                    <= timestamp_seconds_to_datetime(data.get("closing_time"))
                )

        return False

    @property
    def time_until_close(self) -> timedelta:
        """
        Get time until close of the venue.

        Returns
        -------
        timedelta
            Returns the time until close. Uninitialized if not available

        """
        day = current_time().strftime("%Y-%m-%d")
        if self.opening_days is None:
            self.update_opening_days()

        for data in self.opening_days:
            if day == data.get('day_iso'):
                return timestamp_seconds_to_datetime(
                    data.get("closing_time")) - current_time()

        self.update_opening_days()
        for data in self.opening_days:
            if day == data.get('day_iso'):
                return timestamp_seconds_to_datetime(
                    data.get("closing_time")) - current_time()

        return timedelta()

    @property
    def time_until_open(self) -> timedelta:
        """
        Get time until the market opens.

        Returns
        -------
        timedelta
            Returns the time until open. Uninitialized if not available

        """
        day = current_time().strftime("%Y-%m-%d")
        if self.opening_days is None:
            self.update_opening_days()

        for data in self.opening_days:
            if day == data.get('day_iso'):
                return timestamp_seconds_to_datetime(
                    data.get("opening_time")) - current_time()

        self.update_opening_days()
        for data in self.opening_days:
            if day == data.get('day_iso'):
                return timestamp_seconds_to_datetime(
                    data.get("opening_time")) - current_time()

        return timedelta()

    def update_opening_days(self):
        """Update the opening_days property of the TradingVenue instances."""
        self.opening_days = self._request(
            endpoint=f"venues/{self.mic}/opening-days").get("results")
