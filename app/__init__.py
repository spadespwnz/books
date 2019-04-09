from flask import Flask
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv

load_dotenv(".env")
mongoUri = os.getenv("MONGO_DB_URI")

# from . import config_default
# config = config_default.DevConfig
app = Flask(__name__, static_folder="./public", template_folder="./static")
app.config["MONGO_URI"] = mongoUri
app.config.from_object(os.environ.get("FLASK_ENV") or "config_default.DevConfig")
mongo = PyMongo(app)
# app.config["DB"] = mongo
from app.routes import page_routes
from app.routes.api.api import api_blueprint

app.register_blueprint(api_blueprint, url_prefix="/api")
