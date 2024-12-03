import duckdb
from typing import TypedDict


class Match(TypedDict):
    taxonID: int
    vernacularName: str
    canonicalName: str
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

    # Reassign rank to species if taxonRank is subspecies
    if rank == 'subspecies':
        rank = 'species'

    if rank == 'species':
        try:
            genus = taxon.split(' ')[0]
            species = taxon.split(' ')[1]
        except ValueError:
            print("A species should be in the following format: '<genus> <species>'")

        # Reassign rank to genus if sp. is listed as species
        if species == 'sp.':
            rank = 'genus'
            taxon = genus

    query = (
        f"""
            SELECT taxonID, genus, specificEpithet, infraspecificEpithet, vernacularName, canonicalName,
            (jaro_winkler_similarity('{genus}', genus) + jaro_winkler_similarity('{species}', specificEpithet)) / 2
            AS similarity 
            FROM df 
            WHERE taxonRank = 'species' AND similarity > 0.95
            ORDER BY similarity 
        """
        if rank == 'species'
        else f"""
            SELECT taxonID, canonicalName, vernacularName,
            jaro_winkler_similarity('{taxon}', canonicalName) 
            AS similarity,
            FROM df
            WHERE taxonRank = '{rank}'
            ORDER BY similarity 
        """
    )

    match = duckdb.query(query).df()

    if match.empty: return None

    match = match.sort_values('similarity', ascending=False).head(1).to_dict(orient="records")[0]
    match = match if match['similarity'] > threshold else None

    return match




