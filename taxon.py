"""
Reads Taxon.tsv from GBIF taxonomic backbone as a pandas DataFrame.

Transforms dataset for fuzzy matching and merging with Vernaculars.tsv.

Meant to import taxa, i.e.:
    >>> from taxon import taxa
"""


import pandas as pd
import os
from dotenv import load_dotenv


load_dotenv()
taxon_path = os.getenv('TAXON_PATH')

cols = {
    'taxonID': 'Int64',
    'acceptedNameUsageID': 'Int64',
    'canonicalName': 'string',
    'genericName': 'string',
    'specificEpithet': 'string',
    'infraspecificEpithet': 'string',
    'taxonRank': 'string',
    'kingdom': 'string',
    'phylum': 'string',
    'class': 'string',
    'order': 'string',
    'family': 'string',
    'genus': 'string'
}


taxa = pd.read_csv(
    '/Users/dmarkbreiter/Downloads/backbone (1)/Taxon.tsv.zip',
    sep='\t',
    on_bad_lines='skip',
    keep_default_na=False,
    usecols=list(cols.keys()),
    #dtype=cols,
    engine='pyarrow'
)

accepted_ids = taxa['acceptedNameUsageID'].to_list()
taxon_ids = taxa['taxonID'].to_list()
taxa['taxonID'] = [i if i else t for t, i in zip(taxon_ids, accepted_ids)]

