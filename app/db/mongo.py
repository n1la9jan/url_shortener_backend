from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from app.config import MONGO_URI, DB_NAME, COLLECTION_NAME

_client = None
_db = None
_collection = None

def init_db():
    global _client, _db, _collection
    try:
        _client = MongoClient(MONGO_URI)
        _db = _client[DB_NAME]
        _collection = _db[COLLECTION_NAME]
        print("Connected to MongoDB")
    except ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")
        exit(1)


def get_collection():
    if _collection is None:
        raise Exception("MongoDB not initialized. Call init_db() first.")
    return _collection
def get_db():
    if _collection is None:
        raise Exception("MongoDB not initialized. Call init_db() first.")
    return _db
def get_client():
    if _client is None:
        raise Exception("MongoDB not initialized. Call init_db() first.")
    return _client 