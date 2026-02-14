import json
import re
from rapidfuzz import process, fuzz

team_map = json.load(open("app/mappings/team_mapping.json"))

TEAM_NAMES = list(team_map.keys())
CACHE = {}
NORMALIZED_NAME_TO_TEAMS = {}

SIM_THRESHOLD = 80
STOP_WORDS = {"fc", "cf", "sc", "afc", "cfc", "club", "the"}
TOKEN_ALIASES = {
    "utd": "united",
    "st": "saint",
    "manchester": "man",
}

MANUAL_ALIASES = {
    "psg": "Paris SG",
    "paris saint germain": "Paris SG",
}



def _normalize_team_name(name: str) -> str:
    lowered = re.sub(r"[^a-z0-9\s]", " ", name.lower())
    tokens = []
    for token in lowered.split():
        if token in STOP_WORDS:
            continue
        tokens.append(TOKEN_ALIASES.get(token, token))
    return " ".join(tokens)


for team in TEAM_NAMES:
    normalized = _normalize_team_name(team)
    NORMALIZED_NAME_TO_TEAMS.setdefault(normalized, []).append(team)


def match_team(name: str) -> str:

    normalized_name = _normalize_team_name(name)

    alias_match = MANUAL_ALIASES.get(normalized_name)
    if alias_match:
        CACHE[normalized_name] = alias_match
        return alias_match

    # cached
    if normalized_name in CACHE:
        return CACHE[normalized_name]

    # exact
    if name in team_map:
        CACHE[normalized_name] = name
        return name

    normalized_exact = NORMALIZED_NAME_TO_TEAMS.get(normalized_name)
    if normalized_exact and len(normalized_exact) == 1:
        CACHE[normalized_name] = normalized_exact[0]
        return normalized_exact[0]

    # fuzzy search
    match, score, _ = process.extractOne(
        normalized_name,
        list(NORMALIZED_NAME_TO_TEAMS.keys()),
        scorer=fuzz.WRatio,
    )

    # reject weak matches
    if score < SIM_THRESHOLD:
        return None

    candidates = NORMALIZED_NAME_TO_TEAMS.get(match, [])
    if len(candidates) != 1:
        return None

    resolved_match = candidates[0]

    # reject if no shared word
    if not set(normalized_name.split()) & set(match.split()):
        return None

    CACHE[normalized_name] = resolved_match
    return resolved_match
