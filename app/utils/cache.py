from functools import lru_cache
@lru_cache(maxsize=128)
def get_cached_value(code: str):
    from app.db.mongo import get_collection
    collection = get_collection()
    entry = collection.find_one({"code": code})
    return entry['url'] if entry else None
