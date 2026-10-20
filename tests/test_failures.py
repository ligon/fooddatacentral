from fooddatacentral import search, nutrients, ingredients
import pandas as pd
import unittest, warnings
from unittest import mock

# These tests fake the USDA API, so they need no network or API key.

def response(status, payload=None):
    r = mock.Mock(status_code=status)
    r.json.return_value = payload or {}
    return r

FOOD = {'foodNutrients': [{'type': 'FoodNutrient', 'amount': 2.0,
                           'nutrient': {'name': 'Protein', 'unitName': 'g'}}]}

class TestFailures(unittest.TestCase):
    def setUp(self):
        for f in (search, nutrients, ingredients):
            f.cache_clear()
        warnings.simplefilter("always")

    def test_search_failure_is_empty_dataframe(self):
        """
        Test that a failed search returns an empty DataFrame, with a warning
        """
        with mock.patch('requests.get', return_value=response(500)):
            with warnings.catch_warnings(record=True) as w:
                actual = search('key', 'avocado')
        self.assertIsInstance(actual, pd.DataFrame)
        self.assertTrue(actual.empty)
        self.assertEqual(len(w), 1)

    def test_ingredients_missing_food(self):
        """
        Test that ingredients returns None for an unknown fdc_id
        """
        with mock.patch('requests.get', return_value=response(404)):
            with warnings.catch_warnings(record=True) as w:
                self.assertIsNone(ingredients('key', 1))
        self.assertEqual(len(w), 1)

    def test_failure_not_cached(self):
        """
        Test that a failed request is retried rather than remembered
        """
        with mock.patch('requests.get', side_effect=[response(500), response(200, FOOD)]):
            self.assertIsNone(nutrients('key', 1))
            self.assertEqual(nutrients('key', 1).loc['Protein', 'Quantity'], 2.0)

    def test_success_cached(self):
        """
        Test that a successful request is not repeated
        """
        with mock.patch('requests.get', return_value=response(200, FOOD)) as get:
            nutrients('key', 1)
            nutrients('key', 1)
        self.assertEqual(get.call_count, 1)

    def test_cached_result_not_shared(self):
        """
        Test that changing a returned DataFrame doesn't change later results
        """
        with mock.patch('requests.get', return_value=response(200, FOOD)):
            first = nutrients('key', 1)
            first.loc['Protein', 'Quantity'] = 99
            self.assertEqual(nutrients('key', 1).loc['Protein', 'Quantity'], 2.0)

if __name__ == '__main__':
    unittest.main()
