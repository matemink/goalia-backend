import requests, os
from app.cache import matches_cache
from app.predictor import predict_matches

API_TOKEN = os.getenv("FOOTBALL_TOKEN")

def update_data():
    url = "https://api.football-data.org/v4/matches"
    headers = {"X-Auth-Token": API_TOKEN}
    r = requests.get(url, headers=headers, timeout=10)

    data = r.json()
    matches_cache.clear()
    matches_cache.extend(data.get("matches", []))

    predict_matches(matches_cache)