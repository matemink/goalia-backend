matches_cache = []
predictions_cache = {}

# Mutable container to avoid global rebinding across modules.
last_updated = {"value": None}
