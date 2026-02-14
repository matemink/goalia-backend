from app.team_matcher import match_team
import json

# load mappings once
team_map = json.load(open("app/mappings/team_mapping.json"))
league_map = json.load(open("app/mappings/league_mapping.json"))


def build_features(match: dict):
    """
    Converts API match → ML feature vector
    Safe matching with fuzzy + validation
    """

    home_raw = match["homeTeam"]["name"]
    away_raw = match["awayTeam"]["name"]
    league_raw = match["competition"]["name"]

    # resolve team names safely
    home_name = match_team(home_raw)
    away_name = match_team(away_raw)

    # fallback if not matched
    home_id = team_map.get(home_name, 0) if home_name else 0
    away_id = team_map.get(away_name, 0) if away_name else 0

    league_id = league_map.get(league_raw, 0)

    # feature vector must match training order
    return [
        home_id,
        away_id,
        league_id,

        # rolling stats placeholders
        0.0,  # home_avg_scored
        0.0,  # home_avg_conceded
        0.0,  # home_winrate
        0.0,  # home_goal_diff_form

        0.0,  # away_avg_scored
        0.0,  # away_avg_conceded
        0.0,  # away_winrate
        0.0   # away_goal_diff_form
    ]
