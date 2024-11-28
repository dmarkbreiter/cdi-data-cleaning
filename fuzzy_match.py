import pandas as pd
import duckdb
from time import time
import polars as pl
from rapidfuzz import fuzz

df = pd.read_csv('data/vernaculars.csv')

def match_polars(taxon:str):
    vernaculars = pl.read_csv(
        'data/vernaculars-cleaned.csv',
        dtypes={"taxonID": pl.Float64}
    )

    # Compute the fuzzy match scores
    vernaculars = vernaculars.with_columns(
        vernaculars["canonicalName"].map(lambda x: fuzz.ratio(x, taxon)).alias("match_score")
    )

    # Get the row with the highest match score
    highest_match = vernaculars.filter(pl.col("match_score") == vernaculars["match_score"].max())

    return highest_match


def match_duck_db(taxon:str, rank='species', threshold=0.95):
    rank = rank.lower()
    taxon = taxon.replace("'", '').replace('"', '')
    if rank == 'species':

        try:
            genus = taxon.split(' ')[0]
            species = taxon.split(' ')[1]
        except ValueError:
            print("A species should be in the following format: '<genus> <species>'")

        match = duckdb.query(
            f"""
            SELECT taxonID, genus, specificEpithet, vernacularName, canonicalName,
            (jaro_winkler_similarity('{genus}', genus) + jaro_winkler_similarity('{species}', specificEpithet)) / 2
            AS similarity 
            FROM df 
            WHERE taxonRank = 'species'
            ORDER BY similarity 
            DESC LIMIT 1
            """
        ).df()
    else:
        match = duckdb.query(
            f"""
            SELECT taxonID, canonicalName, vernacularName,
            jaro_winkler_similarity('{taxon}', canonicalName) 
            AS similarity,
            FROM df
             WHERE taxonRank = '{rank}'
            ORDER BY similarity 
            DESC LIMIT 1
            """
        ).df()

    if match.empty:
        return ''

    match = match.sort_values('similarity', ascending=False).head(1).to_dict(orient="records")[0]
    match = match if match['similarity'] > threshold else ''

    return match

match = match_duck_db('Thorius spilogasteri')

print(match)



