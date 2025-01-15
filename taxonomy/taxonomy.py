import pandas as pd
from .join import vernaculars
from .fuzzy_match import fuzzy_match


def create_records(data):
    # Remove unneeded columns from emu df
    cols = [col for col in data if col not in ['taxon', 'taxon_irn', 'department']]
    emu_dropped = data.drop(cols, axis=1)

    # Join based on canonicalName
    joined = pd.merge(emu_dropped, vernaculars, left_on='taxon', right_on='canonical_name')
    joined = joined.drop_duplicates(subset=['taxon'], keep='first')
    joined['similarity'] = 1.0
    #return joined.to_dict(orient="records")
    return joined.set_index("taxon").to_dict(orient="index")


class Taxonomy:
    def __init__(self, data):
        self.records = create_records(data)
        self.duplicate_count = 0
        self.unique_count = 0

    def match(self, taxon: str, rank: str, irn: int, department: str, threshold=0.95) -> None:
        """Adds taxon to taxonomy dictionary"""
        if not taxon:
            return None

        # match = self._get(taxon)
        match = self.records.get(taxon)

        if match:
            # return self.add(taxon, rank, irn, department, match)
            self.duplicate_count += 1
            return match


        else:
            self.unique_count += 1
            match = fuzzy_match(vernaculars, taxon, rank, threshold=threshold)
            if match:
                return self.add(taxon, rank, irn, department, match)

    def add(self, taxon: str, rank: str, irn: int, department: str, match: dict) -> None:
        """Adds taxon to taxonomy dictionary"""
        self.records[taxon] = {
            'taxon': taxon,
            'taxon_irn': irn,
            'taxon_rank': rank,
            'department': department.lower(),
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
        # self.records.append(match)
        return match

    def _get(self, taxon, rank):
        match = [r for r in self.records if r['taxon'] == taxon and r['taxon_rank'] == rank]
        if match:
            return match[0]
        else:
            return None

    def get_match(self, taxon: str):
        """Returns a list of matches from taxonomy records (does not perform fuzzy match if match does nto exist)"""
        match = [r for r in self.records if r['taxon'] == taxon]
        return match

    def save_records(self, path):
        df = pd.DataFrame.from_dict(self.records, orient='index')
        df.fillna('', inplace=True)
        df.to_csv(path)
    
    def to_df(self):
        df = pd.DataFrame.from_dict(self.records, orient='index')
        df.fillna('', inplace=True)
        return df


