import json
from rapidfuzz import process, fuzz

team_map = json.load(open("app/mappings/team_mapping.json"))

TEAM_NAMES = list(team_map.keys())
CACHE = {}

SIM_THRESHOLD = 90


def match_team(name: str) -> str:

    # cached
    if name in CACHE:
        return CACHE[name]

    # exact
    if name in team_map:
        CACHE[name] = name
        return name

    # fuzzy search
    match, score, _ = process.extractOne(
        name,
        TEAM_NAMES,
        scorer=fuzz.token_sort_ratio
    )

    # reject weak matches
    if score < SIM_THRESHOLD:
        return None

    # reject if no shared word
    if not set(name.lower().split()) & set(match.lower().split()):
        return None

    CACHE[name] = match
    return match
