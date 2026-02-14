from catboost import CatBoostClassifier
import json
from app.cache import predictions_cache
from app.features import build_features

model = CatBoostClassifier()
model.load_model("app/models/goalia_catboost.cbm")

team_map = json.load(open("app/mappings/team_mapping.json"))
league_map = json.load(open("app/mappings/league_mapping.json"))

def predict_matches(matches):
    predictions_cache.clear()

    for m in matches:
        x = [build_features(m, team_map, league_map)]
        probs = model.predict_proba(x)[0]

        predictions_cache[m["id"]] = {
            "home": float(probs[0]),
            "draw": float(probs[1]),
            "away": float(probs[2]),
            "confidence": float(max(probs))
        }