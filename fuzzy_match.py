import duckdb


def fuzzy_match(df, taxon:str, rank='species', threshold=0.95):
    if not taxon or not rank: return ('', '')

    rank = rank.lower()
    taxon = taxon.replace("'", '').replace('"', '')

    if rank == 'species':
        try:
            genus = taxon.split(' ')[0]
            species = taxon.split(' ')[1]
        except ValueError:
            print("A species should be in the following format: '<genus> <species>'")

        # Reassign rank to genus if sp. is listed as species
        rank = 'genus' if species == 'sp.' or species == 'sp' else 'species'

    match =(
        f"""
            SELECT taxonID, genus, specificEpithet, vernacularName, canonicalName,
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

    match = duckdb.query(match).df()

    if match.empty: return ''

    match = match.sort_values('similarity', ascending=False).head(1).to_dict(orient="records")[0]
    match = match if match['similarity'] > threshold else ''

    return match




