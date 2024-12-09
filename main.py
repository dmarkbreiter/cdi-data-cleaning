import pandas as pd
from fuzzy_match import fuzzy_match
from time import time
from tqdm import tqdm
from join import vernaculars
from emu import emu
import os


# Remove unneeded columns from emu df
cols = [col for col in emu if col not in ['taxon', 'taxonIrn']]
emu_dropped = emu.drop(cols, axis=1)

# Join based on canonicalName
joined = pd.merge(emu_dropped, vernaculars, left_on='taxon', right_on='canonicalName')
joined = joined.drop_duplicates(subset=['taxon'], keep='first')

# Create dictionary and taxa list
# vernaculars_taxa_joined = pd.merge(vernaculars, taxa, on='taxonID', how='left')
vernacular_dict = joined.set_index('taxon').to_dict(orient="index")
taxa = list(zip(emu['taxon'], emu['taxonRank'], emu['taxonIrn']))


# Main logic for assigning vernacular name
def get_vernacular(taxon: str, rank, irn: int):
    empty_row = ('', '', '')

    if not taxon:
        return empty_row

    match = vernacular_dict.get(taxon)

    if match:
        return (match['vernacularName'], match['taxonID'], irn)

    else:
        match = fuzzy_match(vernaculars, taxon, rank)
        if match:
            vernacular_dict[taxon] = {
                'taxonIrn': irn,
                'taxonID': match['taxonID'],
                'kingdom': match['kingdom'],
                'phylum': match['phylum'],
                'class': match['class'],
                'order': match['order'],
                'family': match['family'],
                'genus': match['genus'],
                'specificEpithet': match['specificEpithet'],
                'infraspecificEpithet': match['infraspecificEpithet'],
                'vernacularName': match['vernacularName'],
                'canonicalName': match['canonicalName'],
                'similarity': match['similarity']
            }
            return (match['vernacularName'], match['taxonID'], irn)
        return empty_row



start_time = time()

results = [
    get_vernacular(taxon[0], taxon[1], taxon[2])
    for taxon in tqdm(taxa, desc="Matching EMu taxa to vernacular names")
]

results = pd.DataFrame(results, columns=['vernacularName', 'taxonID', 'taxonIrn'])

print(time() - start_time)

# Save results
emu['vernacularName'] = results['vernacularName'].to_list()
emu['taxonID'] = results['taxonID'].to_list()
emu['taxonIrn'] = results['taxonIrn'].to_list()

emu.to_csv('data/emu-matched.csv')

# Save dictionary
vernacular_dict_df = pd.DataFrame.from_dict(vernacular_dict, orient='index')
vernacular_dict_df.fillna('', inplace=True)
vernacular_dict_df.to_csv('data/vernacular_dict.csv')
