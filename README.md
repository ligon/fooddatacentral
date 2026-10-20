

# FoodDataCentral

[![img](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.7020171-blue.svg)](https://doi.org/10.5281/zenodo.7020171)

The USDA maintains a database of nutritional information, where
different kinds of food are identified by an FDC number.  They do
not provide any data on prices.

To look up nutritional information, use api provided by the USDA at
<https://fdc.nal.usda.gov/>.   You should sign up for a
free api key (see directions on page), then add that key here in
place of "DEMO\_KEY".

    apikey = "DEMO_KEY"  # Replace with a real key!  "DEMO_KEY" will be slow...


## Looking up foods

I've written a little module `fooddatacentral` with the methods

-   `search`
-   `nutrients`
-   `ingredients`
-   `units`


## FDC Search

Here's a little code to help look up FDC codes for foods of
different descriptions.

    import fooddatacentral as fdc
    
    fdc.search(apikey,"crunchy peanut butter")


## FDC Nutrients

Once we know the `fdc_id` of a particular food we can look up a
variety of information on it.  We start with nutrients

    id =     # Put an FDC ID HERE!
    fdc.nutrients(apikey,fdc_id=id)


## FDC Ingredients

We can also look up the ingredients for many foods (specifically Survey Foods) in the FDC:

    
    fdc.ingredients(apikey,id)


## Versioning

Releases follow [Semantic Versioning](https://semver.org/).  The public API is the
functions `search`, `nutrients`, `ingredients` and `units`: their
arguments and the kinds of values they return.  Anything else in the
package may change without notice.

-   A **major** release (2.0.0) changes the public API incompatibly.
-   A **minor** release (1.1.0) adds features, or drops support for a
    Python version that has reached end of life.
-   A **patch** release (1.1.1) only fixes bugs.

So a dependency like `fooddatacentral>=1.1,<2` will not pick up a
release that breaks your code.  Releases before 1.1.0 did not follow
this scheme.

