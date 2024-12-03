"""
Script to merge GBIF taxononmic backbone Taxon.tsv and VernacularName.tsv, on taxonID.

Meant to import vernaculars, i.e.:
    >>> from join import vernaculars
"""


import pandas as pd
from vernaculars import vernaculars
from taxon import taxa

# Clean
cols = [col for col in vernaculars.columns if col not in ['taxonID', 'vernacularName', 'source', 'weight']]
vernaculars.drop(cols, axis=1, inplace=True)

# Merge
vernaculars = pd.merge(vernaculars, taxa, on='taxonID', how='left')
