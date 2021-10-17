import unittest
from os import getenv

from lemon_markets.account import Account
from lemon_markets.instrument import Instruments


client_id = getenv('CLIENT_ID')
client_token = getenv('CLIENT_TOKEN')


class _TestInstrument(unittest.TestCase):
    def setUp(self):
        self.acc = Account(client_id, client_token)

    def test_search_instrument(self):
        instr = Instruments(self.acc)
        tsla = instr.list_instruments(search='Tesla', type='stock')[0]
        self.assertEqual(tsla.isin, 'US88160R1014')


if __name__ == '__main__':
    unittest.main()
