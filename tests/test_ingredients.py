import os
from fooddatacentral import ingredients
import pandas as pd 
import unittest, warnings


apikey = os.environ.get("FDC_API_KEY")

@unittest.skipUnless(apikey, "set FDC_API_KEY to test against the USDA API")
class TestIngredients(unittest.TestCase):
    def test_warn1(self):
        """
        Test that it returns a warning for branded foods
        """
        #2107531 = CEREAL; Branded food
        #173889 = Cereals ready-to-eat, POST, Honeycomb Cereal; SR legacy food
        warnings.simplefilter("always")
        with warnings.catch_warnings(record=True) as w:
            ingredients(apikey, 2107531)
            self.assertEqual(len(w), 1)
            
    def test_warn2(self):
        """
        Test that it returns an emptylist and a warning for  SR legacy foods
        """
        #173889 = Cereals ready-to-eat, POST, Honeycomb Cereal; SR legacy food
        actual= ingredients(apikey, 173889)
        expect = []
        self.assertEqual(expect, actual)
        
        ingredients.cache_clear()  # A cached call returns without warning
        warnings.simplefilter("always")
        with warnings.catch_warnings(record=True) as w:
            ingredients(apikey, 173889)
            self.assertEqual(len(w), 1)
if __name__ == '__main__':
    unittest.main()
