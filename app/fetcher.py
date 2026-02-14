import json
import os
import time
from pathlib import Path

import requests

from app.cache import last_updated, matches_cache

API_TOKEN = os.getenv("FOOTBALL_TOKEN")
CACHE_FILE = Path("app/data/matches_cache.json")
API_URL = "https://api.football-data.org/v4/matches"
DEFAULT_TIMEOUT = 10


def _ensure_cache_dir() -> None:
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)


def _save_cache_to_disk() -> None:
    _ensure_cache_dir()
    payload = {
        "updated_at": last_updated["value"],
        "matches": matches_cache,
    }
    CACHE_FILE.write_text(json.dumps(payload), encoding="utf-8")


def _load_cache_from_disk() -> bool:
    if not CACHE_FILE.exists():
        return False

    payload = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    matches = payload.get("matches", [])
    updated_at = payload.get("updated_at")

    matches_cache.clear()
    matches_cache.extend(matches)
    last_updated["value"] = updated_at
    return True


def update_data() -> bool:
    if not API_TOKEN:
        return False

    headers = {"X-Auth-Token": API_TOKEN}
    response = requests.get(API_URL, headers=headers, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()

    data = response.json()
    matches_cache.clear()
    matches_cache.extend(data.get("matches", []))
    last_updated["value"] = int(time.time())
    _save_cache_to_disk()
    return True


def get_matches_with_cache(ttl_seconds: int, force_refresh: bool = False) -> dict:
    now = int(time.time())

    if not matches_cache:
        _load_cache_from_disk()

    is_cache_fresh = (
        last_updated["value"] is not None
        and now - last_updated["value"] <= ttl_seconds
    )

    if force_refresh or not is_cache_fresh:
        try:
            updated = update_data()
        except requests.RequestException:
            updated = False

        if not updated and not matches_cache:
            _load_cache_from_disk()

    return {
        "source": "cache" if last_updated["value"] and now - last_updated["value"] <= ttl_seconds else "stale-cache",
        "cached_at": last_updated["value"],
        "matches": matches_cache,
    }
