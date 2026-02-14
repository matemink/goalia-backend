import time
from fastapi import FastAPI
from app.fetcher import update_data
from app.cache import matches_cache, predictions_cache

app = FastAPI()

# ===== CACHE SETTINGS =====
CACHE_TTL = 60  # seconds
last_update = 0


# ===== STARTUP LOAD =====
@app.on_event("startup")
def startup():
    global last_update
    update_data()
    last_update = time.time()


# ===== MAIN ENDPOINT =====
@app.get("/api/matches")
def get_matches():
    global last_update

    # refresh cache if expired
    if time.time() - last_update > CACHE_TTL:
        update_data()
        last_update = time.time()

    return {
        "matches": matches_cache,
        "predictions": predictions_cache
    }


# ===== HEALTH CHECK =====
@app.get("/")
def health():
    return {
        "status": "ok",
        "cached_matches": len(matches_cache),
        "cached_predictions": len(predictions_cache),
        "last_update_seconds_ago": int(time.time() - last_update)
    }
