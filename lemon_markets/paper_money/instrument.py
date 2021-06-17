from lemon_markets.helpers.api_object import ApiObject


class Instrument(ApiObject):

    class Values(ApiObject.Values):
        isin: str = None
        wkn: str = None
        name: str = None
        title: str = None
        symbol: str = None
        type: str = None
        currency: str = None
        tradable: bool = None

    def __init__(self, data: dict):
        self._update_values(data)

    @property
    def isin(self):
        return self.Values.isin

    @property
    def wkn(self):
        return self.Values.wkn

    @property
    def name(self):
        return self.Values.name

    @property
    def title(self):
        return self.Values.title

    @property
    def symbol(self):
        return self.Values.symbol

    @property
    def type(self):
        return self.Values.type

    @property
    def currency(self):
        return self.Values.currency

    @property
    def tradable(self):
        return self.Values.tradable


class ListInstruments(ApiObject):

    class Values(ApiObject.Values):
        instruments: [Instrument] = []

    class BodyVariables(ApiObject.BodyVariables):
        tradable: bool = None
        search: str = None
        currency: str = None
        type: str = None
        limit: int = None
        offset: int = None

    def __init__(self):
        self._update_values()
