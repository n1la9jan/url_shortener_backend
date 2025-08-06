from flask import Flask, request, redirect, jsonify
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os, random, string
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    print("Connected to MongoDB")
except ConnectionFailure as e:
    print(f"Could not connect to MongoDB: {e}")
    exit(1)
#base62 encoding for short codes

BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encode_base62(num):
    if num == 0:
        return BASE62_ALPHABET[0]
    base62 = []
    while num > 0:
        num, rem = divmod(num, 62)
        base62.append(BASE62_ALPHABET[rem])
    return ''.join(reversed(base62))

def get_next_id():
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
    '''
    # Alternative random code generation
    chars = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choice(chars) for i in range(length))
        if collection.find_one({"code": code}) is None:
            return code
            '''
    return code




@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    #check existence of the URL
    existing_entry = collection.find_one({"url": data['url']})
    if existing_entry:
        code = existing_entry['code']
        new_url = f"{request.host_url}{code}"
        return jsonify({"new_url": new_url}), 200

    url = data['url']
    if not url.startswith(('http://', 'https://')):
        return jsonify({"error": "URL must start with http:// or https://"}), 400

    #generating the short code
    code = generate_short_code()

    #adding the url and code to the database
    try:
        collection.insert_one({"url": url, "code": code})
    except Exception as e:  
        return jsonify({"error": str(e)}), 500

    new_url = f"{request.host_url}{code}"
    return jsonify({"new_url": new_url}), 201


@app.route('/<code>', methods=['GET'])
def redirect_to_url(code):
    entry = collection.find_one({"code": code})
    if entry:
        return redirect(entry['url'], code=302)
    else:
        return jsonify({"error": "URL not found"}), 404

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)