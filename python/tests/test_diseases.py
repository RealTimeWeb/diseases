import unittest

import sys

sys.path.append("../src")

try:
    import diseases
except ImportError:
    from python.src import diseases


class TestDiseases(unittest.TestCase):
    def test_method_online(self):
        diseases.connect()
        diseases._start_editing()

        keys = ['year', 'week', 'state', 'disease', 'cases']

        item = diseases.get_diseases_information("STATE==VIRGINIA")
        self.assertTrue(isinstance(item, list))

        # Assert all of the keys are in item
        intersection = set(keys).intersection(item[0])
        self.assertEqual(5, len(intersection))

        diseases._save_cache("../src/diseases_cache.json")

    def test_method_offline(self):
        diseases.disconnect("../src/diseases_cache.json")

        keys = ['year', 'week', 'state', 'disease', 'cases']

        item = diseases.get_diseases_information("STATE==VIRGINIA")
        self.assertTrue(isinstance(item, list))

        # Assert all of the keys are in item
        intersection = set(keys).intersection(item[0])
        self.assertEqual(5, len(intersection))

    def test_throw_exception(self):
        diseases.connect()

        with self.assertRaises(diseases.DiseasesException) as context:
            diseases.get_diseases_information("Hello")

        self.assertEqual('Make sure you entered a valid query',
                         context.exception.args[0])

        with self.assertRaises(diseases.DiseasesException) as context:
            diseases.get_diseases_information(1)

        self.assertEqual('Please enter a valid query',
                         context.exception.args[0])

        with self.assertRaises(diseases.DiseasesException) as context:
            diseases.get_diseases_information("USA==USA")

        self.assertEqual('There were no results', context.exception.args[0])
