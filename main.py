import pandas as pd
from fuzzy_match import match_duck_db
from time import time
from tqdm import tqdm

emu = pd.read_csv('data/cdi-biology-650k.csv')
vernaculars = pd.read_csv('data/vernaculars-cleaned.csv')

cols = [col for col in emu if col != 'taxon']
emu_dropped = emu.drop(cols, axis=1)

joined = pd.merge(emu_dropped, vernaculars, left_on='taxon', right_on='canonicalName')
joined = joined.drop_duplicates(subset=['taxon'], keep='first')
joined = joined.drop(['Unnamed: 0'], axis=1)

vernacular_dict = joined.set_index('taxon').to_dict(orient="index")
taxa = list(zip(emu['taxon'], emu['taxonRank']))[0:999]



def get_vernacular(taxon:str, rank):
    match = vernacular_dict.get(taxon)

    if match:
        return (match['vernacularName'], match['taxonID'])

    else:
        match = match_duck_db(taxon, rank)
        if match:
            vernacular_dict[taxon] = {
                'taxonID': match['taxonID'],
                'vernacularName': match['vernacularName'],
                'canonicalName': match['canonicalName'],
                'similarity': match['similarity']
            }
            return (match['vernacularName'], match['taxonID'])
        return ('', '')



start_time = time()
results = [
    get_vernacular(taxon[0], taxon[1])
    for taxon in tqdm(taxa, desc="Matching EMu taxa to vernacular names")
]

results = pd.DataFrame(results, columns=['vernacularName', 'taxonID'])

print(time() - start_time)
print(results)