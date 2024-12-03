import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
vernaculars_path = os.getenv('VERNACULAR_PATH')

cols = {
    'taxonID': 'Int64',
    'vernacularName': 'string',
    'language': 'string',
    'source': 'string'
}

vernacular_names = pd.read_csv(
    vernaculars_path,
    sep='\t',
    on_bad_lines='skip',
    keep_default_na=False,
    usecols=list(cols.keys()),
    dtype=cols
)

vernacular_names = vernacular_names.query("language == 'en'")


def assign_source_weight(source):
    weights = {
        "IOC World Bird List, v13.2": 5,
        "The Paleobiology Database": 5,
        "Checklist of Vermont Species": 4,
        "Martha's Vineyard species checklist": 4,
        "Multilingual IOC World Bird List, v11.2": 3,
        "Catalogue of Life Checklist": 2,
        "The IUCN Red List of Threatened Species": 1
    }

    # Return weight based on weights dict, 0 if the source is not in dict
    return weights.get(source, 0)


weight = [assign_source_weight(source) for source in vernacular_names['source'].to_list()]
vernacular_names['weight'] = weight

sorted_vernaculars = vernacular_names.sort_values(by='weight', axis=0, ascending=False)

vernaculars = sorted_vernaculars.drop_duplicates(subset=['taxonID'], keep='first')
