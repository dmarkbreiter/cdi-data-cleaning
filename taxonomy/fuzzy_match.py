 import duckdb
from typing import TypedDict
import pandas as pd


class Match(TypedDict):
    taxon_id: int
    vernacular_name: str
    canonical_name: str
    similarity: float


def fuzzy_match(df, taxon: str, rank='species', threshold=0.95) -> Match | None:
    """
    Returns a fuzzy match using the Jaro-Winkler similarity algoroithm from the GBIF Taxon from the GBIF backbone.

    Parameters:
        df (pd.DataFrame): Dataframe output from the join.py file merged with .
        taxon (str): Taxon to be matched with taxonomic backbone
        rank (str): taxonRank dwc equivalent
        threshold (float): Similarity indexed filter (anything below the threshold will not be returned)

    Returns:
        None: If no suitable match is made
        Match: A dictionary of returned fields from the backbone

    Example:
        >>> fuzzy_match(df, 'Rana sp.', rank='species')
        {'taxonID': 2422253, 'canonicalName': 'Rana', 'vernacularName': 'Green Frog', 'similarity': 0.95}
    """

    if not taxon or not rank: return None

    rank = rank.lower()
    taxon = taxon.replace("'", '').replace('"', '')
    columns = """
        taxon_id, 
        kingdom, 
        phylum, 
        class, 
        "order", 
        family, 
        genus, 
        specific_epithet, 
        infraspecific_epithet, 
        vernacular_name, 
        canonical_name
    """

    if ' sp.' in taxon and rank == 'species':
        rank = 'genus'
        taxon = taxon.split(' ')[0]

    if rank == 'subspecies':
        try:
            genus = taxon.split(' ')[0]
            species = taxon.split(' ')[1]
            subspecies = taxon.split(' ')[2]
        except ValueError:
            print("A subspecies should be in the following format: '<genus> <species> <subspecies>'")

        query = f"""
            SELECT {columns},
            jaro_winkler_similarity('{genus}', genus) AS genus_similarity,
            jaro_winkler_similarity('{species}', specific_epithet) AS species_similarity,
            jaro_winkler_similarity('{subspecies}', specific_epithet) AS species_similarity,
            (
                jaro_winkler_similarity('{genus}', genus) + 
                jaro_winkler_similarity('{species}', specific_epithet) +
                jaro_winkler_similarity('{subspecies}', specific_epithet)
            ) / 3 AS similarity 
            FROM df 
            WHERE taxon_rank = 'species' 
            AND jaro_winkler_similarity('{genus}', genus) > {threshold}
            AND jaro_winkler_similarity('{species}', specific_epithet) > {threshold}
            AND jaro_winkler_similarity('{subspecies}', specific_epithet) > {threshold}
            ORDER BY similarity 
        """

    elif rank == 'species':
        try:
            genus = taxon.split(' ')[0]
            species = taxon.split(' ')[1]
        except ValueError:
            print("A species should be in the following format: '<genus> <species>'")

        query = f"""
            SELECT {columns},
            jaro_winkler_similarity('{genus}', genus) AS genus_similarity,
            jaro_winkler_similarity('{species}', specific_epithet) AS species_similarity,
            (
                jaro_winkler_similarity('{genus}', genus) + 
                jaro_winkler_similarity('{species}', specific_epithet)
            ) / 2 AS similarity 
            FROM df
            WHERE taxon_rank = 'species'
              AND jaro_winkler_similarity('{genus}', genus) > {threshold}
              AND jaro_winkler_similarity('{species}', specific_epithet) > {threshold}
            ORDER BY genus_similarity DESC, species_similarity DESC;
        """

    else:
        query = f"""
            SELECT {columns},
            jaro_winkler_similarity('{taxon}', canonical_name) 
            AS similarity,
            FROM df
            WHERE taxon_rank = '{rank}'
            ORDER BY similarity 
        """

    match = duckdb.query(query).df()

    if match.empty: return None

    if not isinstance(match, pd.DataFrame):
        print('hi~')

    match = match.sort_values('similarity', ascending=False).head(1).to_dict(orient="records")[0]

    # Only return a match if it's similarity score is above threshold
    if match['similarity'] > threshold:
        match['vernacular_name'] = match['vernacular_name'].capitalize()
        return match
    else:
        return None
