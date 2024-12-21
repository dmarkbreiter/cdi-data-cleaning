import pandas as pd
from time import time
from tqdm import tqdm
from match.matcher import Matcher
from emu import emu


taxa = list(zip(emu['taxon'], emu['taxonRank'], emu['taxonIrn']))[0:1000]
start_time = time()

matcher = Matcher(emu)

results = [
    matcher.get_vernacular(taxon[0], taxon[1], taxon[2])
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
matcher.save_dict('data/matched-dict.csv')
