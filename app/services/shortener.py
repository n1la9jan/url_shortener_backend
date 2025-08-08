from app.db.mongo import get_db
from app.utils.encode import encode_base62


def get_next_id():
    db = get_db()
    counter = db.counters.find_one_and_update(
        {'_id': 'url_id'},
        {'$inc': {'seq': 1}},
        upsert=True,
        return_document=True
    )
    return counter['seq']


def generate_short_code():
    next_id = get_next_id()
    code = encode_base62(next_id)
    return code