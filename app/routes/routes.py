from flask import request, redirect, jsonify, Blueprint
from app.db.mongo import get_collection
from app.services.shortener import generate_short_code
from app.utils.sanitize import sanitize_url

url_blueprint = Blueprint('url', __name__)
@url_blueprint.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    collection = get_collection()
    
    
    if not data or 'url' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    raw_url = data['url'].strip()
    if not raw_url.startswith(('http://', 'https://')):
        return jsonify({"error": "URL must start with http:// or https://"}), 400


    sanitized_url = sanitize_url(raw_url)

    if not sanitized_url:
        return jsonify({"error": "Invalid URL"}), 400    
    #check existence of the URL
    existing_entry = collection.find_one({"url": sanitized_url})
    if existing_entry:
        code = existing_entry['code']
        new_url = f"{request.host_url}{code}"
        return jsonify({"new_url": new_url}), 200


    #generating the short code
    code = generate_short_code()

    #adding the url and code to the database
    try:
        collection.insert_one({"url": sanitized_url, "code": code})
    except Exception as e:  
        return jsonify({"error": str(e)}), 500

    new_url = f"{request.host_url}{code}"
    return jsonify({"new_url": new_url}), 201


@url_blueprint.route('/<code>', methods=['GET'])
def redirect_to_url(code):
    
    collection = get_collection()
    entry = collection.find_one({"code": code})
    if entry:
        return redirect(entry['url'], code=302)
    else:
        return jsonify({"error": "URL not found"}), 404