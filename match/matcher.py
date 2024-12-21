import pandas as pd
from .join import vernaculars
from .fuzzy_match import fuzzy_match



def create_dict(data):
    # Remove unneeded columns from emu df
    cols = [col for col in data if col not in ['taxon', 'taxonIrn']]
    emu_dropped = data.drop(cols, axis=1)

    # Join based on canonicalName
    joined = pd.merge(emu_dropped, vernaculars, left_on='taxon', right_on='canonicalName')
    joined = joined.drop_duplicates(subset=['taxon'], keep='first')

    return joined.set_index('taxon').to_dict(orient="index")


class Matcher:
    def __init__(self, data):
        self.dict = create_dict(data)
        self.taxa =  list(zip(data['taxon'], data['taxonRank'], data['taxonIrn']))

    def get_vernacular(self, taxon: str, rank: str, irn: int):
        empty_row = ('', '', '')

        if not taxon:
            return empty_row

        match = self.dict.get(taxon)
        if match:
            return (match['vernacularName'], match['taxonID'], irn)

        else:
            match = fuzzy_match(vernaculars, taxon, rank)
            if match:
                self.dict[taxon] = {
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
        
    def save_dict(self, path):
        df = pd.DataFrame.from_dict(self.dict, orient='index')
        df.fillna('', inplace=True)
        df.to_csv(path)
    
    def to_df(self):
        df = pd.DataFrame.from_dict(self.dict, orient='index')
        df.fillna('', inplace=True)
        return df