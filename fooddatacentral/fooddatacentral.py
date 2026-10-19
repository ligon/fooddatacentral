from urllib.request import Request, urlopen
import pandas as pd
import json
from json import JSONDecodeError
import warnings
import os
import numpy as np
import requests
from functools import lru_cache, wraps
from pint import UnitRegistry, UndefinedUnitError, DimensionalityError

ureg = UnitRegistry()

home = os.path.expanduser('~')
unitrc = ('unitsrc',os.path.join(home,'.unitsrc'))

for fn in unitrc:
    try:
        ureg.load_definitions(fn)
        break
    except (IOError, ValueError):
        pass


class _Failed(Exception):
    """A lookup failed: warn with the message and return value instead."""
    def __init__(self, message, value=None):
        super().__init__(message)
        self.value = value


def _cached(fn):
    """
    Cache fn like lru_cache, but don't cache failures and don't share results.

    fn raises _Failed rather than returning a failure, so a transient
    error is retried on the next call instead of being remembered.
    Callers get a copy of each cached result, so changing it doesn't
    change what later calls return.
    """
    cached = lru_cache(maxsize=256)(fn)

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            result = cached(*args, **kwargs)
        except _Failed as e:
            warnings.warn(str(e))
            return e.value
        return result.copy() if result is not None else None

    wrapper.cache_info = cached.cache_info
    wrapper.cache_clear = cached.cache_clear
    return wrapper


@_cached
def search(apikey, term, url = 'https://api.nal.usda.gov/fdc/v1/search',num_results=50):
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
    pageSize : int
        Number of results to return per page.  Default is 50.

    Returns
    -------
        a pd.DataFrame of matches; empty if there are none or the request fails.
    """
    parms = (('format', 'json'),('generalSearchInput', term),('api_key', apikey),('pageSize',num_results))
    r = requests.get(url, params = parms)
    if r.status_code == 200:
        if 'foods' in r.json():
            l = r.json()['foods']
        else:
            raise _Failed("No foods found for '%s'." % term, pd.DataFrame())
    elif r.status_code == 404:
        raise _Failed("Couldn't find %s." % term, pd.DataFrame())
    else:
        raise _Failed("Some problem with request: %s" % str(r), pd.DataFrame())

    return pd.DataFrame(l)

@_cached
def nutrients(apikey, fdc_id, url = 'https://api.nal.usda.gov/fdc/v1/food/',verbose=False):
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

        if r.status_code == 200:
            L = r.json()['foodNutrients']
        elif r.status_code == 404:
            raise _Failed("Couldn't find fdc_id=%s." % fdc_id)
        else:
            raise _Failed("Some problem with request: %s" % str(r))
        if verbose: print(r.headers)
    except KeyError:
        raise _Failed("No nutrient data for fdc_id=%s." % fdc_id)

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
        return ureg.Quantity(np.nan,'ml')

    try:
        return x.to(ureg.hectogram)
    except DimensionalityError:
        return x.to(ureg.deciliter)

@_cached
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

        if r.status_code == 200:
            L = r.json()['inputFoods']
        elif r.status_code == 404:
            raise _Failed("Couldn't find fdc_id=%s." % fdc_id)
        else:
            raise _Failed("Some problem with request: %s" % str(r))
    except KeyError:
        raise _Failed("Make sure it's a Survey Food (FNDDS); couldn't find fdc_id=%s." % fdc_id)
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
