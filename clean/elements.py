def clean_element(element: str) -> str:
    """Cleans EMu element column and transforms into dwc:element"""

    if not element: 
        return ''
    
    cleaned_val = element.replace('?', '').strip().lower()

    elements = {
        # Vertebrates
        "pygidium": "pygidium",
        "rib": "rib",
        "vertebra": "vertebrae",
        "cervix": "cervix",
        "femur": "femur",
        "humerus": "humerus",
        "phalange": "phalange",
        "tibia": "tibia",
        "fibula": "fibula",
        "metatarsa": "metatarsus",
        "metacarpa": "metacarpus",
        "tarsometatarsus": "tarsometatarsus",
        "tibiotarsus": "tibiotarsus",
        "phalanx": "phalanx",
        "hypopharynx": "hypopharynx",
        "pharynx": "pharynx",
        "radius": "radius",
        "ulna": "ulna",
        "ischium": "ischium",
        "pubis": "pubis",
        "ilium": "ilium",
        "scapula": "scapula",
        "coracoid": "coracoid",
        "interclavicle": "interclavicle",
        "clavicle": "clavicle",
        "prosternum": "prosternum",
        "sternum": "sternum",
        "chevron": "chevron",
        "skull": "skull",
        "premaxilla": "premaxillae",
        "maxilla": "maxillae",
        "premaxilla": "premaxillae",
        "dentary": "dentary",
        "quadrate": "quadrate",
        "squamosal": "squamosal",
        "egg": "egg",
        "spiracle": "spiracle",
        "adult": "adult",
        "mouth part": "mouth part",
        "labrum": "labrum",
        "labium": "labium",
        "palp": "palp",
        "proboscis": "proboscis",
        "labellum": "labellum",
        "labrum": "labrum",
        "head": "head",
        "ovary": "ovary",
        "osteoderm": "osteoderm",
        "scale": "scale",
        "scute": "scute",
        "ocellus": "eye",
        "tusk": "tusk",
        "coprolite": "coprolite",
        "sesamoid": "sesamoid",
        "calcaneum": "calcaneum",
        "ossicle": "ossicle",
        "crania": "cranium",
        "cranium": "cranium",


        # Invertebrates
        "antenna": "antenna",
        "shell": "shell",
        "test": "test",
        "plate": "plate",
        "colony": "colony",
        "valve": "valve",
        "corallite": "corallite",
        "wing": "wing",
        "cephalon": "cephalon",
        "carapace": "carapace",
        "cranidium": "cranidium",
        "operculum": "operculum",
        "ovipositor": "ovipositor",
        "appendage": "appendage",
        "pronotum": "pronotum",
        "elytron": "elytron",
        "rhodolith": "rhodolith",
        "odolith": "odolith",
        "hypostome": "hypostome",
        "glabella": "glabella",
        "scutellum": "scutellum",
        "corallum": "corallum",
        "telson": "telson",
        "claw": "claw",
        "arm": "arm",
        "calyx": "calyx",
        "crown": "crown",
        "cercus": "cercus",
        "flagellum": "flagellum",
        "cranidium": "cranidium",
        "tergite": "tergite",
        "sternite": "sternite",
        "sclerite": "sclerite",
        "cauda": "caudae",
        "metasternum": "metasternum",
        "leg": "leg",
        "prothorax": "prothorax",
        "protothorax": "protothorax",
        "mesothorax": "mesothorax",
        "metathorax": "metathorax",
        "abdomen": "abdomen",
        "thorax": "thorax",
        "puparium": "puparium",
        "pupal case": "pupal case",
        "pupal exuviae": "pupal exuviae",
        "pupal exuvium": "pupal exuviae",
        "pupal skin": "pupal skin",
        "pupal shell": "pupal shell",
        "pupa": "pupa",
        "skin": "skin",
        "spine": "spine",
        "synsacrum": "synsacrum",
        "tergum": "tergum",
        "glabella": "glabella",
        "pygidium": "pygidium",
        "tooth": "tooth",
        "teeth": "tooth",
        "denticle": "tooth",
        "jaw": "jaw",
        "metacoxa": "leg",
        "metanotum": "metanotum",
        "mandible": "mandible",
        "coxite": "coxite",
        "malleolar": "malleolar",
        "magnum": "magnum",
        "tendon": "tendon",
        "trochanter": "trochanter",
        "pelvis": "pelvis",
        "entocuneiform": "entocuneiform",
        "naviculocuboid": "naviculocuboid",
        "urostyle": "urostyle",
        "skeleton": "skeleton",
        "horn": "horn",
        "dentary": "dentary",
        "dentaries":"dentary",
        "urohyal": "urohyal",
        "metapodial": "metapodial",
        "carpometacarpus": "carpometacarpus",
        "metacarpal": "metacarpal",
        "scaphoid": "scaphoid",
        "fin": "fin",
        "trackway": "trackway",
        "antler": "antler",
        "unciform": "unciform",
        "navicular": "navicular",
        "pisiform": "pisiform",
        "baculum": "baculum",
        "patella": "patella",
        "Ectocuneiform": "ectocuneiform",
        "astragalus": "astragalus",
        "antler": "antler",
        "trapezoid": "trapezoid",
        "palatine": "palatine",
        "ceratohyals": "ceratohyals",
        "rostrum": "rostrum",
        "sternebra": "sternebra",
        "epiplastron": "epiplastron",
        "xiphiplastron": "xiphiplastron",
        "hyoplastron": "hyoplastron",
        "hypoplastron": "hypoplastron",
        "cleithrum": "cleithrum",
        "entoplastron": "entoplastron",
        "plastron": "plastron",
        "mesocuneiform": "mesocuneiform",
        "pterygoid": "pterygoid",
        "feather": "feather",
        "suprapygal": "suprapygal",
        "pygal": "pygal",
        "furcula": "furcula",
        "acetabulum": "acetabulum",
        "preopercular": "preopercular",
        "opercular": "opercular",
        "leaf": "leaf",
        "frond": "frond",
        "bone": "bone",
        "vomer": "vomer",
        "navicula": "navicula",
        "malleolus": "malleolus",
    }


    match = ''

    for element in elements.keys():
        if element in cleaned_val:
            matched_element = f'{element};' if match else element
            match += matched_element
            break

    return match

