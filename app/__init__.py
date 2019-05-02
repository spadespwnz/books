from flask import Flask
from flask_pymongo import PyMongo
from flask_redis import Redis
import os
from dotenv import load_dotenv

mongo = PyMongo()
redis = Redis()


def create_app(config=None, db_uri=None):
    load_dotenv(".env")
    mongoUri = db_uri or os.getenv("MONGO_DB_URI")
    if not os.getenv("JWT_SECRET"):
        print("No JWT_SECRET ENV VARIABLE FOUND. USING DEFAULT, THIS IS UNSAFE")

    jwt_key = os.getenv("JWT_SECRET") or "somedefaultkey"

    flask_app = Flask(__name__, static_folder="./public", template_folder="./static")
    flask_app.config.from_object(
        config or os.environ.get("FLASK_ENV") or "config_default.DevConfig"
    )
    if "MONGO_URI" not in flask_app.config:
        flask_app.config["MONGO_URI"] = mongoUri
    flask_app.config["REDIS_HOST"] = "localhost"
    flask_app.config["REDIS_PORT"] = 6379
    flask_app.config["REDIS_DB"] = 0
    mongo.init_app(flask_app)
    redis.init_app(flask_app)
    flask_app.jwt_key = jwt_key
    # app.config["DB"] = mongo
    from app.routes.page_routes import page_blueprint
    from app.routes.api.api import api_blueprint as user_login_api
    from app.routes.api.user_api import api_blueprint as user_api
    from app.routes.api.book_api import api_blueprint as book_api
    from app.routes.api.profile_api import api_blueprint as profile_api
    flask_app.register_blueprint(user_login_api, url_prefix="/api")
    flask_app.register_blueprint(user_api, url_prefix="/api")
    flask_app.register_blueprint(book_api, url_prefix="/api/books")
    flask_app.register_blueprint(profile_api, url_prefix="/api/profile")
    flask_app.register_blueprint(page_blueprint)
    flask_app.config["host"]="0.0.0.0"
    return flask_app


app = create_app()
