from setuptools import setup, find_packages
from os.path import abspath, dirname, join

README_MD = open(join(dirname(abspath(__file__)), "README.md")).read()

setup(
    name="fooddatacentral",
    version="1.0.5",
    packages=find_packages(exclude="tests"),

    description="Python module to obtain information from the USDA's Food Data Central data project.",
    long_description=README_MD,
    long_description_content_type="text/markdown",

    url="https://github.com/ligon/fooddatacentral",

    author_name="Ethan Ligon",
    author_email="ligon@berkeley.edu",

    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3 :: Only"
    ],

    keywords="USDA, FDC",
)
