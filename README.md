# Lemon Markets API Access

This is a Python SDK for accessing the Lemon Markets API.
API documentation can be found here: https://documentation.lemon.markets/

## Installation

```
git clone https://github.com/LinusReuter/lemon-markets-api-access.git
python setup.py install
```


## Usage

### Authentication

For getting started the account must be initialized. 
The account is needed for further requests.
Your access_token is automatically updated when it expires.

```python
from lemon_markets.account import Account

account = Account(your_client_id, your_client_secret)

#for seeing your accsess token
print(account.access_token)
```

### State and Space


```python
from lemon_markets.state import State

state = State(account)

#get the balance of the state (all money not given to spaces)
print(state.balance) 

#get your space (because your client ID is linked to a Space the request "list Spaces" only contains one space.)
space = state.spaces[0]
print(space.state) #the state of the space as dict like in the API response.
#the elements of the state as floats:
print(space.balance)
print(space.cash_to_invest)
```

### Instruments
```python
from lemon_markets.paper_money.instrument import *

#getting a list of all Instruments matching the query params 
#(all arguments are an option and not needed)
instruments = Instruments(account).list_instruments(tradable=true/false, search="Name/Title, WKN, Symbol or ISIN", currency="", type="one of the following:" ("stock", "bond", "fond", "ETF" or "warrant"))

#get a singe instrument by isin:
instrument = Instruments(account).get_instrument(isin="")

#to get the information of an instrument use:
instrument.isin
instrument.wkn
instrument.name
instrument.title
instrument.type
instrument.symbol
instrument.currency
instrument.tradable
instrument.trading_venues
```
