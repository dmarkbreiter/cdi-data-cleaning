"""
Reads Vernacular.tsv from GBIF taxonomic backbone as a pandas DataFrame.

Transforms dataset for fuzzy matching and merging with Taxon.tsv. Druplicates are dropped based on canonicalName
and assigned weight based on source.

Meant to import vernaculars, i.e.:
    >>> from match.vernaculars import vernaculars
"""


import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
vernaculars_path = os.getenv('VERNACULAR_PATH')

cols = {
    'taxonID': 'Int64',
    'vernacularName': 'string',
    'language': 'string',
    'source': 'string'
}

vernacular_names = pd.read_csv(
    vernaculars_path,
    sep='\t',
    on_bad_lines='skip',
    keep_default_na=False,
    usecols=list(cols.keys()),
    dtype=cols
)

vernaculars = vernacular_names.query("language == 'en'")


def assign_source_weight(source):
    weights = {
        "IOC World Bird List, v13.2": 5,
        "The Paleobiology Database": 5,
        "Checklist of Vermont Species": 4,
        "Martha's Vineyard species checklist": 4,
        "Multilingual IOC World Bird List, v11.2": 3,
        "Catalogue of Life Checklist": 2,
        "The IUCN Red List of Threatened Species": 1
    }

    # Return weight based on weights dict, 0 if the source is not in dict
    return weights.get(source, 0)


weight = [assign_source_weight(source) for source in vernaculars['source'].to_list()]
vernaculars = vernaculars.assign(weight=weight)

