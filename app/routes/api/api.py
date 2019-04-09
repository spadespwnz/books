from flask import Blueprint
from flask import current_app as app
from app import mongo

api_blueprint = Blueprint("api", __name__)


@api_blueprint.route("/", methods=["GET"])
def api():
    for doc in mongo.db.books.find():
        print(doc)
    return "Api Version: " + app.config.get("VERSION")
