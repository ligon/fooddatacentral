from fooddatacentral import nutrients
import pandas as pd 
import unittest

apikey = "kY45fKdbAFHas9GpxBKlDyEYbwvfC00z17oKd3ba"

class TestNutrients(unittest.TestCase):
    def test_column(self):
        """
        Test that it returns a df with the desirable columns
        """
        #171705 = Avocados, raw, all commercial varieties
        expected = ['Quantity', 'Units']
        actual = nutrients(apikey,171705)
        self.assertEqual(expected, actual.columns.tolist())	
    
    def test_reasonable(self):
        """
        Test that it returns a df with reasonable nutrient quantities and units
        """
        #171705 = Avocados, raw, all commercial varieties
        result  = nutrients(apikey,171705)
        actual_q = result.loc['Energy', 'Quantity']
        actual_u = result.loc['Energy', 'Units']
        expected_u = ['kJ', 'kiloJoule ', 'kj', 'kilojoule ']
        self.assertTrue(0 <= actual_q<= 1000)	
        self.assertTrue(actual_u in expected_u)	

if __name__ == '__main__':
    unittest.main()
