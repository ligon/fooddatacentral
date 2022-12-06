# FoodDataCentral
[![DOI](https://zenodo.org/badge/238808020.svg)](https://zenodo.org/badge/latestdoi/238808020)

The USDA maintains a database of nutritional information, where
different kinds of food are identified by an FDC number.  They do
not provide any data on prices.

To look up nutritional information, use api provided by the USDA at
<https://fdc.nal.usda.gov/>.   You should sign up for a
free api key (see directions on page), then add that key here in
place of &ldquo;DEMO<sub>KEY</sub>&rdquo;.

    apikey = "DEMO_KEY"  # Replace with a real key!  "DEMO_KEY" will be slow...


<a id="org0a001b6"></a>

# Looking up foods

I&rsquo;ve written a little module `fooddatacentral` with the methods

-   `search`
-   `nutrients`
-   `units`


<a id="org24e646d"></a>

# FDC Search

Here&rsquo;s a little code to help look up FDC codes for foods of
different descriptions.

    import fooddatacentral as fdc
    
    fdc.search(apikey,"crunchy peanut butter")


<a id="org4e9bac2"></a>

# FDC Nutrients

Once we know the `fdc_id` of a particular food we can look up a
variety of information on it.  We start with nutrients

    id =     # Put an FDC ID HERE!
    fdc.nutrients(apikey,fdc_id=id)


<a id="org7462d48"></a>

# FDC Ingredients

We can also look up the ingredients for many foods (specifically Survey Foods) in the FDC:

    
    fdc.ingredients(apikey,id)

