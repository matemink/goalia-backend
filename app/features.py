import json
import re

from rapidfuzz import fuzz, process

from app.team_matcher import match_team

# load mappings once
team_map = json.load(open("app/mappings/team_mapping.json"))
league_map = json.load(open("app/mappings/league_mapping.json"))

LEAGUE_SIM_THRESHOLD = 85
LEAGUE_STOP_WORDS = {"liga", "league", "division", "div", "the"}
LEAGUE_ALIASES = {
    "primeira": "portugal",
}
MANUAL_LEAGUE_ALIASES = {
    "primera": "La Liga",
    "primeira liga": "Liga Portugal",
}


def _normalize_league_name(name: str) -> str:
    lowered = re.sub(r"[^a-z0-9\s]", " ", name.lower())
    tokens = []
    for token in lowered.split():
        if token in LEAGUE_STOP_WORDS:
            continue
        tokens.append(LEAGUE_ALIASES.get(token, token))
    return " ".join(tokens)


NORMALIZED_LEAGUE_TO_NAMES = {}
for league_name in league_map:
    normalized = _normalize_league_name(league_name)
    NORMALIZED_LEAGUE_TO_NAMES.setdefault(normalized, []).append(league_name)


def _resolve_league_name(league_raw: str) -> str | None:
    if league_raw in league_map:
        return league_raw

    normalized = _normalize_league_name(league_raw)

    manual_alias = MANUAL_LEAGUE_ALIASES.get(normalized)
    if manual_alias:
        return manual_alias

    exact_normalized = NORMALIZED_LEAGUE_TO_NAMES.get(normalized)
    if exact_normalized and len(exact_normalized) == 1:
        return exact_normalized[0]

    match = process.extractOne(
        normalized,
        list(NORMALIZED_LEAGUE_TO_NAMES.keys()),
        scorer=fuzz.WRatio,
    )
    if not match:
        return None

    matched_name, score, _ = match
    if score < LEAGUE_SIM_THRESHOLD:
        return None

    candidates = NORMALIZED_LEAGUE_TO_NAMES.get(matched_name, [])
    if len(candidates) != 1:
        return None

    return candidates[0]


def build_features(match: dict):
    """
    Converts API match into the same 3-feature vector used in training:
    [home_team_enc, away_team_enc, league_enc]
    """

    home_raw = match["homeTeam"]["name"]
    away_raw = match["awayTeam"]["name"]
    league_raw = match["competition"]["name"]

    # resolve team names safely
    home_name = match_team(home_raw)
    away_name = match_team(away_raw)

    # fallback to 0 for unknown mapping values
    home_id = team_map.get(home_name, 0) if home_name else 0
    away_id = team_map.get(away_name, 0) if away_name else 0
    resolved_league = _resolve_league_name(league_raw)
    league_id = league_map.get(resolved_league, 0) if resolved_league else 0

    return [
        float(home_id),
        float(away_id),
        float(league_id),
    ]
