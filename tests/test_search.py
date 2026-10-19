import os
from fooddatacentral import search
import pandas as pd 
import unittest, warnings

apikey = os.environ.get("FDC_API_KEY")

@unittest.skipUnless(apikey, "set FDC_API_KEY to test against the USDA API")
class TestSearch(unittest.TestCase):
    def test_reasonable(self):
        """
        Test that it returns an empty df for an illogical food input
        """
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            actual = search(apikey,"xqzzvbnmk")  # FDC search is fuzzy, so a near-miss like "avocao" still matches
        self.assertEqual(len(w), 0)  # An empty result from a failed request doesn't count
        self.assertTrue(actual.empty)	

    def test_string(self):
        """
        Test that it returns a non-empty df for a string input of food name
        """
        expected = 173573
        actual = search(apikey,"avocado")
        lst = actual['fdcId'].tolist()
        self.assertTrue(expected in lst)	
    
    def test_int(self):
        """
        Test that it returns a non-empty df for an integer input of FDC ID
        """
        expected = 'oil, avocado'
        actual = search(apikey,173573)
        lst = actual['description'].str.lower().tolist()
        self.assertTrue(expected in lst)	

if __name__ == '__main__':
    unittest.main()
