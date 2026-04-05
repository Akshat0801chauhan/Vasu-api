from rapidfuzz import process

# 🔥 Molecules
CHEMISTRY_MAP = {
    "CH4": "methane",
    "H2O": "water",
    "CO2": "carbon",
    "O2": "oxygen",
    "NH3": "ammonia",
}

# 🔥 Element symbols (CASE-SENSITIVE)
ELEMENT_SYMBOL_MAP = {
    "H": "hydrogen",
    "He": "helium",
    "Li": "lithium",
    "Be": "beryllium",
    "B": "boron",
    "C": "carbon",
    "N": "nitrogen",
    "O": "oxygen",
    "F": "fluorine",
    "Na": "sodium",
    "Mg": "magnesium",
    "Al": "aluminium",
    "Si": "silicon",
    "P": "phosphorus",
    "S": "sulfur",
    "Cl": "chlorine",
    "K": "potassium",
    "Ca": "calcium",
    "Fe": "iron",
    "Cu": "copper",
    "Zn": "zinc",
}


def ai_match(query, keyword_map):
    query = query.strip()

    # ✅ 1. EXACT SYMBOL MATCH (CASE-SENSITIVE 🔥)
    if query in ELEMENT_SYMBOL_MAP:
        mapped = ELEMENT_SYMBOL_MAP[query]
        if mapped in keyword_map:
            return [mapped]

    # ✅ 2. MOLECULE MATCH (CASE-SENSITIVE)
    if query in CHEMISTRY_MAP:
        mapped = CHEMISTRY_MAP[query]
        if mapped in keyword_map:
            return [mapped]

    # convert to lowercase for rest
    q = query.lower()

    # ✅ 3. Exact keyword
    if q in keyword_map:
        return [q]

    # ✅ 4. PREFIX MATCH (for lowercase inputs)
    prefix_matches = [
        key for key in keyword_map.keys()
        if key.startswith(q)
    ]
    if prefix_matches:
        return prefix_matches

    # ✅ 5. FUZZY MATCH
    match = process.extractOne(q, keyword_map.keys())
    if match:
        matched_word, score, _ = match
        if score > 70:
            return [matched_word]

    return None