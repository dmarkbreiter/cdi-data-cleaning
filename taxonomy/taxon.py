"""
Reads Taxon.tsv from GBIF taxonomic backbone as a pandas DataFrame.

Transforms dataset for fuzzy matching and merging with Vernaculars.tsv.

Meant to import taxa, i.e.:
    >>> from taxonomy.taxon import taxa
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

taxa.rename(columns={
    'taxonID': 'taxon_id',
    'acceptedNameUsageID': 'accepted_name_usage_id',
    'canonicalName': 'canonical_name',
    'genericName': 'generic_name',
    'specificEpithet': 'specific_epithet',
    'infraspecificEpithet': 'infraspecific_epithet',
    'taxonRank': 'taxon_rank'
}, inplace=True)


accepted_ids = taxa['accepted_name_usage_id'].to_list()
accepted_ids = {*[int(id) for id in accepted_ids if id !='']}

taxon_ids = taxa['taxon_id'].to_list()

# acceptedNameUsageIDs that do not have taxonIDs
difference_ids = list({*accepted_ids} - {*taxon_ids})
difference_ids = [str(id) for id in difference_ids]

# Subset of taxa df if acceptedNameUsageIDs was part of difference
difference_ids_df = taxa[taxa.accepted_name_usage_id.isin(difference_ids)]

# Redefine taxonID as acceptedNameUsageID
accepted_name_ids = [int(id) for id in difference_ids_df['accepted_name_usage_id'].to_list()]
difference_ids_df = difference_ids_df.assign(taxonID=accepted_name_ids)

# Concat frames
taxa = pd.concat([taxa, difference_ids_df])

# taxa['taxonID'] = [accepted if accepted else taxon for taxon, accepted in zip(taxon_ids, accepted_ids)]

