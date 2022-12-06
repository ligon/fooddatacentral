"""
Python module to obtain information from the USDA's Food Data Central data project.

See https://fdc.nal.usda.gov/api-guide.html for API documentation; please also refer to the documentation provided in the README.md.

Optional txt file of units '.unitsrc' can live in the HOME directory with specification of necessary unit conversions (e.g., "extra_large_egg = 56 * grams = xl_egg" and "tea_bag = 3 * grams").

Functions:

    search(str, str/int, url) -> pd.DataFrame
    nutrients(str, int, url) -> pd.DataFrame
    units(int/float, str , ureg) -> ureg
    ingredients(str, int, url) -> pd.DataFrame
"""

from urllib.request import Request, urlopen
import pandas as pd
import json
import warnings
from pint import UnitRegistry, UndefinedUnitError, DimensionalityError
import os 
ureg = UnitRegistry()
home = os.path.expanduser('~')
unit = '.unitsrc'
try:
    ureg.load_definitions(os.path.join(home, unit))
except IOError:
    pass 
import numpy as np


import requests

def search(apikey, term, url = 'https://api.nal.usda.gov/fdc/v1/search'):
    """
    Search Food Central Database, using apikey and "term" as search criterion.
    
    Parameters
    ----------
    apikey : str
        Your personal API key
    term : str, int
        A string of the food name, or a specific FDC ID in int format
    url : str
        default = 'https://api.nal.usda.gov/fdc/v1/search'

    Returns
    -------
        a pd.DataFrame of matches.
    """
    parms = (('format', 'json'),('generalSearchInput', term),('api_key', apikey))
    r = requests.get(url, params = parms)

    if 'foods' in r.json():
        l = r.json()['foods']
    else:
        return []

    return pd.DataFrame(l)

def nutrients(apikey, fdc_id, url = 'https://api.nal.usda.gov/fdc/v1/food/'):
    """
    Construct a food report for food with given fdc_id; nutrients are given per 100 g or 100 ml of the food.
    
    Parameters
    ----------
    apikey : str
        Your personal API key
    fdc_id : int
        a specific FDC ID in int format
    url : str
        default = 'https://api.nal.usda.gov/fdc/v1/search'

    Returns
    -------
        a pd.DataFrame of nutrients and quantities.
    """
    params = (('api_key', apikey),)
    try:
        r = requests.get(url+"%s" % fdc_id, params = params)

        L = r.json()['foodNutrients']
    except KeyError:
        warnings.warn("Couldn't find fdc_id=%s." % fdc_id)
        return None

    v = {}
    u = {}
    for l in L:
        if l['type'] == "FoodNutrient":
            try:
                v[l['nutrient']['name']] = l['amount']  # Quantity
            except KeyError: # No amount?
                v[l['nutrient']['name']] = 0
                
            u[l['nutrient']['name']] = l['nutrient']['unitName']  # Units

    #print(l)
    N = pd.DataFrame({'Quantity':v,'Units':u})

    return N

def units(q,u,ureg=ureg):
    """Convert quantity q of units u to 100g or 100ml."""
    try:
        x = ureg.Quantity(float(q),u)
    except UndefinedUnitError:
        return ureg.Quantity(np.NaN,'ml')

    try:
        return x.to(ureg.hectogram)
    except DimensionalityError:
        return x.to(ureg.deciliter)

def ingredients(apikey, fdc_id, url = 'https://api.nal.usda.gov/fdc/v1/food/'):
    """
    Given fdc_id of a Survey Food, return ingredients of food.
    
    Parameters
    ----------
    apikey : str
        Your personal API key
    fdc_id : int
        a specific FDC ID in int format; should be a Survey Food
    url : str
        default = 'https://api.nal.usda.gov/fdc/v1/search'

    Returns
    -------
        a pd.DataFrame of ingredients and quantities.
    """
    params = (('api_key', apikey),)
    try:
        r = requests.get(url+"%s" % fdc_id, params = params)

        L = r.json()['inputFoods']
    except KeyError:
        warnings.warn("Make sure it's a Survey Food (FNDDS); couldn't find fdc_id=%s." % fdc_id)
        return None
    if L == [] and r.json()['dataType']== 'SR Legacy':
        warnings.warn("No ingredients data for this SR Legacy food fdc_id=%s; " % fdc_id)
        return L
    v = []
    c = []
    w = []
    a = []
    for l in L:
        v.append(l['foodDescription'])
        c.append(l['ingredientCode'])
        w.append(l['ingredientWeight'])
        a.append(l['amount'])
    if w != a:
        return pd.DataFrame({'Ingredient':v,'Food Code/NDB Number':c, 'Weight (grams)':w, 'Amount':a})
    return pd.DataFrame({'Ingredient':v,'Food Code/NDB Number':c, 'Weight (grams)':w})
