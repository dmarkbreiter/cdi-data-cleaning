import pandas as pd
from .join import vernaculars
from .fuzzy_match import fuzzy_match



def create_dict(data):
    # Remove unneeded columns from emu df
    cols = [col for col in data if col not in ['taxon', 'taxonIrn', 'department']]
    emu_dropped = data.drop(cols, axis=1)

    # Join based on canonicalName
    joined = pd.merge(emu_dropped, vernaculars, left_on='taxon', right_on='canonicalName')
    joined = joined.drop_duplicates(subset=['taxon'], keep='first')
    joined['similarity'] = 1.0
    return joined.set_index('taxonIrn').to_dict(orient="index")


class Matcher:
    def __init__(self, data):
        self.dict = create_dict(data)
        self.taxa = list(zip(data['taxon'], data['taxonRank'], data['taxonIrn']))

    def match(self, taxon: str, rank: str, irn: int, department: str, threshold=0.95) -> None:
        """Adds taxon to taxonomy dictionary"""
        if not taxon:
            return None

        match = self.dict.get(irn)

        if match:
            return None

        else:
            match = fuzzy_match(vernaculars, taxon, rank, threshold=threshold)
            if match:
                self.dict[taxon] = {
                    'taxonIrn': irn,
                    'taxonRank': rank,
                    'department': department,
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
            else:
                self.dict[taxon] = {
                    'taxonIrn': irn,
                    'taxonRank': rank,
                    'department': department,
                    'taxonID': '',
                    'kingdom': '',
                    'phylum': '',
                    'class': '',
                    'order': '',
                    'family': '',
                    'genus': '',
                    'specificEpithet': '',
                    'infraspecificEpithet': '',
                    'vernacularName': '',
                    'canonicalName': '',
                    'similarity': 0
                }

    def get_match(self, taxon: str):
        """Returns match from taxonomy dict (does not perform fuzzy match if match does nto exist)"""
        match = self.dict.get(taxon)
        return match
        
    def save_dict(self, path):
        df = pd.DataFrame.from_dict(self.dict, orient='index')
        df.fillna('', inplace=True)
        df.to_csv(path)
    
    def to_df(self):
        df = pd.DataFrame.from_dict(self.dict, orient='index')
        df.fillna('', inplace=True)
        return df
