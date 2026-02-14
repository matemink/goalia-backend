from fastapi import FastAPI, Query

from app.fetcher import get_matches_with_cache

app = FastAPI()

CACHE_TTL = 300  # 5 minutes


@app.get("/api/matches")
def get_matches(force_refresh: bool = Query(False, description="Ignore TTL and refresh from external API")):
    return get_matches_with_cache(ttl_seconds=CACHE_TTL, force_refresh=force_refresh)


@app.get("/")
def health():
    result = get_matches_with_cache(ttl_seconds=CACHE_TTL)
    return {
        "status": "ok",
        "cache_ttl_seconds": CACHE_TTL,
        "cached_matches": len(result["matches"]),
        "cached_at": result["cached_at"],
        "source": result["source"],
    }
