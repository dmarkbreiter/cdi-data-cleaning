import pandas as pd
from time import time
from tqdm import tqdm
from taxonomy.taxonomy import Taxonomy
from emu import emu
from clean import *


# Clean EMu data
emu['sex'] = emu['sex'].apply(clean_sex)
emu['caste'] = emu['sex'].apply(clean_caste)
emu['life_stage'] = emu['sex'].apply(clean_life_stage)
emu['element'] = emu['element'].apply(clean_element)
emu['side'] = emu['side'].apply(clean_side)
emu['type_status'] = emu['type_status'].apply(clean_type_status)
emu['department'] = emu['department'].apply(lambda x: x.lower())

# Prepare taxa list to feed into Matcher match method
taxa_df = emu.drop_duplicates(subset='taxon_irn')
taxa = list(zip(taxa_df['taxon'], taxa_df['taxon_rank'], taxa_df['taxon_irn'], taxa_df['department']))

# Initialize matcher
start_time = time()
taxonomy = Taxonomy(emu)

[
    taxonomy.match(taxon[0], taxon[1], taxon[2], taxon[3])
    for taxon in tqdm(taxa, desc="Matching EMu taxa to vernacular names")
]


# Get results
results = taxonomy.to_df()

print(time() - start_time)

emu = emu.drop(columns=['taxon', 'taxon_rank'])
emu.to_csv('data/emu-cleaned.csv')

# Save dictionary
taxonomy.save_records('data/taxonomy.csv')
