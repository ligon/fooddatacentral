from fooddatacentral import ingredients
import pandas as pd 
import unittest, warnings


apikey = "kY45fKdbAFHas9GpxBKlDyEYbwvfC00z17oKd3ba"

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
            self.assertEquals(len(w), 1)
            
    def test_warn2(self):
        """
        Test that it returns an emptylist and a warning for  SR legacy foods
        """
        #173889 = Cereals ready-to-eat, POST, Honeycomb Cereal; SR legacy food
        actual= ingredients(apikey, 173889)
        expect = []
        self.assertEquals(expect, actual)
        
        warnings.simplefilter("always")
        with warnings.catch_warnings(record=True) as w:
            ingredients(apikey, 173889)
            self.assertEquals(len(w), 1)
if __name__ == '__main__':
    unittest.main()
