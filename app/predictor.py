from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from catboost import CatBoostClassifier

from app.features import build_features

MODEL_PATH = "app/models/goalia_catboost.cbm"
RESULT_LABELS = ["H", "D", "A"]
NOT_STARTED_STATUSES = {"SCHEDULED", "TIMED"}

model = CatBoostClassifier()
model.load_model(MODEL_PATH)


def _is_not_started(match: dict) -> bool:
    status = str(match.get("status") or "").upper()
    if status in NOT_STARTED_STATUSES:
        return True

    utc_date = match.get("utcDate")
    if not utc_date:
        return False

    try:
        kickoff = datetime.fromisoformat(utc_date.replace("Z", "+00:00"))
    except ValueError:
        return False

    return kickoff > datetime.now(timezone.utc)


def predict_match(match: dict) -> Optional[dict]:
    if not _is_not_started(match):
        return None

    features = [build_features(match)]
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
        match["prediction"] = predict_match(match)
    return matches
