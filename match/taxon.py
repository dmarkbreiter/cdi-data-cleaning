"""
Reads Taxon.tsv from GBIF taxonomic backbone as a pandas DataFrame.

Transforms dataset for fuzzy matching and merging with Vernaculars.tsv.

Meant to import taxa, i.e.:
    >>> from match.taxon import taxa
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
    taxon_path,
    sep='\t',
    on_bad_lines='skip',
    keep_default_na=False,
    usecols=list(cols.keys()),
    #dtype=cols,
    engine='pyarrow'
)

accepted_ids = taxa['acceptedNameUsageID'].to_list()
accepted_ids = {*[int(id) for id in accepted_ids if id !='']}

taxon_ids = taxa['taxonID'].to_list()

# acceptedNameUsageIDs that do not have taxonIDs
difference_ids = list({*accepted_ids} - {*taxon_ids})
difference_ids = [str(id) for id in difference_ids]

# Subset of taxa df if acceptedNameUsageIDs was part of difference
difference_ids_df = taxa[taxa.acceptedNameUsageID.isin(difference_ids)]

# Redefine taxonID as acceptedNameUsageID
difference_ids_df['taxonID'] = [int(id) for id in difference_ids_df['acceptedNameUsageID'].to_list()]

# Concat frames
taxa = pd.concat([taxa, difference_ids_df])

# taxa['taxonID'] = [accepted if accepted else taxon for taxon, accepted in zip(taxon_ids, accepted_ids)]

