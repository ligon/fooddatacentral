"""Package to obtain information from the USDA's Food Data Central data project.

See https://fdc.nal.usda.gov/api-guide.html for API documentation; see
https://fdc.nal.usda.gov/api-key-signup.html for API key; please also refer to
the documentation provided in the README.md.

Optional txt file of units '.unitsrc' can live in the HOME directory with
specification of necessary unit conversions (e.g., "extra_large_egg = 56 * grams
= xl_egg" and "tea_bag = 3 * grams"). See documentation for the pint package at
https://pint.readthedocs.io/.

Functions:

    search(str, str/int, url) -> pd.DataFrame
    nutrients(str, int, url) -> pd.DataFrame
    units(int/float, str , ureg) -> ureg
    ingredients(str, int, url) -> pd.DataFrame

"""

from .fooddatacentral import *
