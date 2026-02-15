from __future__ import annotations

from catboost import CatBoostClassifier

from app.features import build_features

MODEL_PATH = "app/models/goalia_catboost.cbm"
RESULT_LABELS = ["H", "D", "A"]
model = CatBoostClassifier()
model.load_model(MODEL_PATH)


def predict_match(match: dict) -> dict | None:
    match_features = build_features(match)

    # Skip prediction when at least one encoded feature is unknown.
    # Unknown teams/leagues are encoded as 0 in build_features.
    if any(feature == 0.0 for feature in match_features):
        return None

    features = [match_features]
    probs = model.predict_proba(features)[0]
    winner_idx = int(max(range(len(probs)), key=lambda i: probs[i]))

    return {
        "label": RESULT_LABELS[winner_idx],
        "confidence": float(probs[winner_idx]),
        "probabilities": {
            "H": float(probs[0]),
            "D": float(probs[1]),
            "A": float(probs[2]),
        },
    }


def enrich_matches_with_predictions(matches: list[dict]) -> list[dict]:
    for match in matches:
        prediction = predict_match(match)
        if prediction is None:
            match.pop("prediction", None)
            continue

        match["prediction"] = prediction
    return matches
