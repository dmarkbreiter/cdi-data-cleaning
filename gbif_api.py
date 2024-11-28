import requests
from time import time

def get_taxon_id(taxon:str):
    url = f'https://api.gbif.org/v1/species/match?name={taxon}&rank=SPECIES'
    response = requests.get(url)
    return response.json()


start_time = time()
get_taxon_id('Thorius spilogaster')
print(time() - start_time)