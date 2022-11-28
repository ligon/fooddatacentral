from fooddatacentral import search
import pandas as pd 
import unittest
from warnings import warn 

apikey = "kY45fKdbAFHas9GpxBKlDyEYbwvfC00z17oKd3ba"

class TestSearch(unittest.TestCase):
    def test_reasonable(self):
        """
        Test that it returns an empty df for an illogical food input
        """
        actual = search(apikey,"avocao")
        warn('Invalid term; check spelling of food names or digits of food code')
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
        lst = actual['lowercaseDescription'].tolist()
        self.assertTrue(expected in lst)	

if __name__ == '__main__':
    unittest.main()
