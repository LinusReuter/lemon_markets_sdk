from dataclasses import dataclass
from datetime import timedelta

from lemon_markets.helpers.api_client import _ApiClient
from lemon_markets.account import Account
from lemon_markets.helpers.time_helper import current_time, timestamp_to_datetime


class TradingVenues(_ApiClient):
    """Available trading venues."""

    trading_venues = None

    def __init__(self, account: Account):
        """
        Initialise using the account.

        Parameters
        ----------
        account : Account
            Your auth data

        """
        super().__init__(account=account)

    def get_venues(self):
        """Load the list of trading venues."""
        data = self._request(endpoint='trading-venues/')
        data_rows = data.get("results")
        self.trading_venues = [TradingVenue.from_response(self, data) for data in data_rows]

    def get_opening_days(self, mic):
        # TODO unpolished (returns raw json reponse)
        """
        Get the days till opening of venue.

        Parameters
        ----------
        mic : str
            Id of the venue

        Returns
        -------
        dict
            Raw response data

        """
        return self._request(endpoint=f"trading-venues/{mic}/opening-days")


@dataclass()
class TradingVenue:
    """A trading venue."""

    name: str = None
    title: str = None
    mic: str = None
    opening_days: list = None
    request_class: TradingVenues = None

    @classmethod
    def from_response(cls, request_class, data: dict):
        # TODO should the from_response methods be made private?
        """
        Fill venu data from response.

        Parameters
        ----------
        request_class : TradingVenues
            The TradingVenues object that returned this TradingVenue
        data : dict
            the response data to fill in

        """
        return cls(
            request_class=request_class,
            name=data.get('name'),
            title=data.get('title'),
            mic=data.get('mic')
        )

    @property
    def is_open(self):
        """
        Check if the venue is open.

        Returns
        -------
        bool
            True if the venue is open, False otherwise

        """
        day = current_time().strftime("%Y-%m-%d")
        if self.opening_days is None:
            self.get_opening_days()

        for data in self.opening_days:
            if day == data.get('day_iso'):
                if timestamp_to_datetime(data.get("opening_time")) <= current_time() <= timestamp_to_datetime(
                        data.get("closing_time")):
                    return True
                else:
                    return False

        self.get_opening_days()
        for data in self.opening_days:
            if day == data.get('day_iso'):
                if timestamp_to_datetime(data.get("opening_time")) <= current_time() <= timestamp_to_datetime(
                        data.get("closing_time")):
                    return True
                else:
                    return False

        return False

    @property
    def time_until_close(self):
        """
        Get time until close of the venue.

        Returns
        -------
        timedelta
            Returns the time until close. Uninitialised if not available

        """
        day = current_time().strftime("%Y-%m-%d")
        if self.opening_days is None:
            self.get_opening_days()

        for data in self.opening_days:
            if day == data.get('day_iso'):
                return timestamp_to_datetime(data.get("closing_time")) - current_time()

        self.get_opening_days()
        for data in self.opening_days:
            if day == data.get('day_iso'):
                return timestamp_to_datetime(data.get("closing_time")) - current_time()

        return timedelta()

    @property
    def time_until_open(self):
        """
        Get time until the market opens.

        Returns
        -------
        timedelta
            Returns the time until open. Uninitialised if not available

        """
        day = current_time().strftime("%Y-%m-%d")
        if self.opening_days is None:
            self.get_opening_days()

        for data in self.opening_days:
            if day == data.get('day_iso'):
                return timestamp_to_datetime(data.get("opening_time")) - current_time()

        self.get_opening_days()
        for data in self.opening_days:
            if day == data.get('day_iso'):
                return timestamp_to_datetime(data.get("opening_time")) - current_time()

        return timedelta()

    def get_opening_days(self):
        # TODO am i right here? just a guess really..
        """
        Get the open days of a week.

        Returns
        -------
        List[str]
            The open days of the week

        """
        self.opening_days = self.request_class.get_opening_days(self.mic).get("results")
