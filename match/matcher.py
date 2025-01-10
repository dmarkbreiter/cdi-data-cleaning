import pandas as pd
from .join import vernaculars
from .fuzzy_match import fuzzy_match



def create_dict(data):
    # Remove unneeded columns from emu df
    cols = [col for col in data if col not in ['taxon', 'taxon_irn', 'department']]
    emu_dropped = data.drop(cols, axis=1)

    # Join based on canonicalName
    joined = pd.merge(emu_dropped, vernaculars, left_on='taxon', right_on='canonical_name')
    joined = joined.drop_duplicates(subset=['taxon'], keep='first')
    joined['similarity'] = 1.0
    return joined.set_index('taxon_irn').to_dict(orient="index")


class Matcher:
    def __init__(self, data):
        self.dict = create_dict(data)
        self.taxa = list(zip(data['taxon'], data['taxon_rank'], data['taxon_irn']))

    def match(self, taxon: str, rank: str, irn: int, department: str, threshold=0.95) -> None:
        """Adds taxon to taxonomy dictionary"""
        if not taxon:
            return None

        match = self.dict.get(irn)

        if match:
            return None

        else:
            match = fuzzy_match(vernaculars, taxon, rank, threshold=threshold)
            match = match if match else {}
            self.add(taxon, rank, irn, department, match)

    def add(self, taxon: str, rank: str, irn: int, department: str, match: dict) -> None:
        """Adds taxon to taxonomy dictionary"""
        self.dict[taxon] = {
            'taxon_irn': irn,
            'taxon_rank': rank,
            'department': department,
            'taxon_id': match.get('taxon_id', ''),
            'kingdom': match.get('kingdom', ''),
            'phylum': match.get('phylum', ''),
            'class': match.get('class', ''),
            'order': match.get('order', ''),
            'family': match.get('family', ''),
            'genus': match.get('genus', ''),
            'specific_epithet': match.get('specific_epithet', ''),
            'infraspecific_epithet': match.get('infraspecific_epithet', ''),
            'vernacular_name': match.get('vernacular_name', ''),
            'canonical_name': match.get('canonical_name', ''),
            'similarity': match.get('similarity', 0)
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
