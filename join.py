import pandas as pd

# Read csvs
vernaculars = pd.read_csv('data/vernaculars.csv')
taxa = pd.read_csv('data/taxa_cleaned.csv')

# Clean
vernaculars.fillna('', inplace=True)
taxa.fillna('', inplace=True)
cols = [col for col in vernaculars.columns if col not in ['taxonID', 'vernacularName']]
vernaculars.drop(cols, axis=1, inplace=True)

# Combine IDs with taxonIDs in taxa
ids = taxa['id'].to_list()
taxon_ids = taxa['taxonID'].to_list()
combined_id = [i if i else t for t, i in zip(taxon_ids, ids)]

# Reassign IDs
taxa['taxonID'] = combined_id

# Merge
vernaculars = pd.merge(vernaculars, taxa, on='taxonID', how='left')
vernaculars.to_csv('data/vernaculars-cleaned.csv')
