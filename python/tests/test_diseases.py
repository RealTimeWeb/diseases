import unittest

import sys

sys.path.append("../src")

try:
    import diseases
except ImportError:
    from python.src import diseases


# Embed your own keys for simplicity
CONSUMER_KEY = "your key goes here"
CONSUMER_SECRET = "your key goes here"
ACCESS_TOKEN = "your key goes here"
ACCESS_TOKEN_SECRET = "your key goes here"
# Remove these lines; we just do this for our own simplicity
with open('../src/secrets.txt', 'r') as secrets:
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = \
        [l.strip() for l in secrets.readlines()]


class TestDiseases(unittest.TestCase):
    def test_method_online(self):
        diseases.connect()
        diseases._start_editing()

        keys = ['change_number', 'change_percentage', 'exchange_name',
                'last_trade_date_and_time', 'last_trade_price', 'ticker_name']

        item = diseases.get_("AAPL")
        self.assertTrue(isinstance(item, dict))

        # Assert all of the keys are in item
        intersection = set(keys).intersection(item)
        self.assertEqual(100, len(intersection))

        diseases._save_cache("../src/diseases_cache.json")

    def test_method_offline(self):
        diseases.disconnect("../diseases/diseases_cache.json")

        keys = ['change_number', 'change_percentage', 'exchange_name',
                'last_trade_date_and_time', 'last_trade_price', 'ticker_name']

        item = diseases.get_("AAPL")
        self.assertTrue(isinstance(item, dict))

        # Assert all of the keys are in the stock
        intersection = set(keys).intersection(item)
        self.assertEqual(100, len(intersection))

    def test_throw_exception(self):
        diseases.connect()

        with self.assertRaises(diseases.DiseasesException) as context:
            diseases.get_(["AAPL"])

        self.assertEqual('MSG', context.exception.args[0])

        with self.assertRaises(diseases.DiseasesException) as context:
            diseases.get_(1)

        self.assertEqual('MSG', context.exception.args[0])

        with self.assertRaises(diseases.DiseasesException) as context:
            diseases.get_("INVALID_STOCK")

        self.assertEqual('MSG', context.exception.args[0])
