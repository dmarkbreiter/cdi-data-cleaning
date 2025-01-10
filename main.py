import pandas as pd
from time import time
from tqdm import tqdm
from match.matcher import Matcher
from emu import emu
from clean import *


# Clean EMu data
emu['sex'] = emu['sex'].apply(clean_sex)
emu['caste'] = emu['sex'].apply(clean_caste)
emu['lifeStage'] = emu['sex'].apply(clean_life_stage)
emu['element'] = emu['element'].apply(clean_element)
emu['side'] = emu['side'].apply(clean_side)
emu['typeStatus'] = emu['typeStatus'].apply(clean_type_status)

# Prepare taxa list to feed into Matcher match method
taxa_df = emu.drop_duplicates(subset='taxonIrn')
taxa = list(zip(taxa_df['taxon'], taxa_df['taxonRank'], taxa_df['taxonIrn'], taxa_df['department']))

# Initialize matcher
start_time = time()
matcher = Matcher(emu)

# Perform matches
[
    matcher.match(taxon[0], taxon[1], taxon[2], taxon[3])
    for taxon in tqdm(taxa, desc="Matching EMu taxa to vernacular names")
]

# Get results
results = matcher.to_df()

print(time() - start_time)

emu.to_csv('data/emu-cleaned.csv')

# Save dictionary
matcher.save_dict('data/matched-dict.csv')
