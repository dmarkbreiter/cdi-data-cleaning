"""
Script to merge GBIF taxononmic backbone Taxon.tsv and VernacularName.tsv, on taxonID.

Meant to import vernaculars, i.e.:
    >>> from match.join import vernaculars
"""


import pandas as pd
from .vernaculars import vernaculars
from .taxon import taxa

# Clean
cols = [col for col in vernaculars.columns if col not in ['taxon_id', 'vernacular_name', 'source', 'weight']]
vernaculars.drop(cols, axis=1, inplace=True)

# Merge
vernaculars = pd.merge(taxa, vernaculars, on='taxon_id', how='left')

# Sort by weight and drop duplicates based on first (highest weight)
vernaculars = vernaculars.sort_values(by='weight', axis=0, ascending=False)
vernaculars.drop_duplicates(subset='canonical_name', keep='first')

# Drop unneeded records
vernaculars = vernaculars.query("kingdom == 'Animalia' & canonical_name != ''")

vernaculars.fillna('', inplace=True)

