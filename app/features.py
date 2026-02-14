import json

from app.team_matcher import match_team

# load mappings once
team_map = json.load(open("app/mappings/team_mapping.json"))
league_map = json.load(open("app/mappings/league_mapping.json"))


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
    league_id = league_map.get(league_raw, 0)

    return [
        float(home_id),
        float(away_id),
        float(league_id),
    ]
