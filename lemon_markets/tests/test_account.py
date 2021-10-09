import unittest
from os import getenv

from lemon_markets.account import Account


client_id = getenv('CLIENT_ID')
client_token = getenv('CLIENT_TOKEN')


class _TestAccount(unittest.TestCase):
    def test_token_type(self):
        self.assertEqual(Account(client_id, client_token).access_token_type, 'bearer')


if __name__ == '__main__':
    unittest.main()