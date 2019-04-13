from flask import Flask
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv

mongo = PyMongo()


def create_app(config=None, db_uri=None):
    load_dotenv(".env")
    mongoUri = db_uri or os.getenv("MONGO_DB_URI")
    flask_app = Flask(__name__, static_folder="./public", template_folder="./static")
    flask_app.config.from_object(
        config or os.environ.get("FLASK_ENV") or "config_default.DevConfig"
    )
    if "MONGO_URI" not in flask_app.config:
        flask_app.config["MONGO_URI"] = mongoUri
    mongo.init_app(flask_app)

    # app.config["DB"] = mongo
    from app.routes.page_routes import page_blueprint
    from app.routes.api.api import api_blueprint as user_api

    flask_app.register_blueprint(user_api, url_prefix="/api")
    flask_app.register_blueprint(page_blueprint)
    return flask_app


app = create_app()
