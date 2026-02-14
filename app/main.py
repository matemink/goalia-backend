from fastapi import FastAPI
from app.fetcher import update_data
from app.cache import matches_cache, predictions_cache

app = FastAPI()

@app.on_event("startup")
def startup():
    update_data()

@app.get("/api/matches")
def get_matches():
    return {
        "matches": matches_cache,
        "predictions": predictions_cache
    }