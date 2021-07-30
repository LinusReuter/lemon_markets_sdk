from lemon_markets.helpers.api_client import _ApiClient
from lemon_markets.account import Account

from enum import Enum
from dataclasses import dataclass
from typing import List


class InstrumentType(Enum):
    """
    Class for different instrument types.

    Properties
    ----------
    STOCK : 'stock'
        Instrument of type stock
    BOND : 'bond'
        Of type bond
    FUND : 'fund'
        Of type fund
    WARRANT : 'warrant'
        Of type warrant

    """

    STOCK = 'stock'
    BOND = 'bond'
    FUND = 'fund'
    WARRANT = 'warrant'


@dataclass()
class Instrument:
    # TODO what does the title propertiey mean?
    """
    Represents an instrument.

    Properties
    ----------
    isin : str
        The isin identifier of the instrument
    wkn : str
        The wkn identifier
    name : str
        The name of the instrument
    title : str
        The title
    symbol : str
        The short symbol the instrument
    currency : str
        Abbreviation of the reported currency
    tradable : str
        Whether the instrument can be traded
    trading_venues : list
        Places where this instrument is traded

    Raises
    ------
    ValueError
        Raised if instrument type is not known

    """

    isin: str = None
    wkn: str = None
    name: str = None
    title: str = None
    type: str = None
    symbol: str = None
    currency: str = None
    tradable: str = None
    trading_venues: list = None

    @classmethod
    def _from_response(cls, data: dict):
        try:
            type_ = InstrumentType(data.get('type'))
        except (ValueError, KeyError):
            raise ValueError('Unexpected instrument type: %r' % data.get('type'))

        return cls(
            isin=data.get('isin'),
            wkn=data.get('wkn'),
            name=data.get('name'),
            title=data.get('title'),
            type=type_,
            symbol=data.get('symbol'),
            currency=data.get('currency'),
            tradable=data.get('tradable'),
            trading_venues=data.get('trading_venues')
        )


class Instruments(_ApiClient):
    """Class for searching instruments."""

    def __init__(self, account: Account):
        """
        Initialise with an account.

        Parameters
        ----------
        account : Account
            The account object

        """
        super().__init__(account=account)

    def list_instruments(self, **kwargs) -> List[Instrument]:
        # TODO what does search mean?
        """
        List all instruments with matching criteria.

        Parameters
        ----------
        tradable : bool, optional
            Search for tradable instruments.
        search : str, optional
            A search term
        currency : str, optional
            A specific currency
        type : str, optional
            A type (`stock`, `bond`, `fund` or `warrant`)

        Returns
        -------
        List[Instrument]
            List of instruments matching your query

        """
        data_rows = self._request_paged('instruments/', params=kwargs)
        return [Instrument._from_response(data) for data in data_rows]
