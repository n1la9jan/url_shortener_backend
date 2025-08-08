from flask import Flask
from flask_cors import CORS
from .db.mongo import init_db
from .routes.routes import url_blueprint

def create_app():

    app = Flask(__name__)
    CORS(app)
    init_db()
    app.register_blueprint(url_blueprint)
    return app