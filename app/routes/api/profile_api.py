from flask import Blueprint, jsonify, Response, request
from flask import current_app as app
from bson import json_util, ObjectId
import json
from app import mongo
from app.Messages import Messages
import app.routes.api.wrappers as wrap

api_blueprint = Blueprint("profile_api", __name__)

@api_blueprint.route("/to_read_list/get", methods=["POST"])
def api_get_to_read_list():
    req_data = request.get_json()
    username = req_data.get("username")
    to_read_list = mongo.db.users.find_one({"username":username},{"to_read_list":1})
    print(to_read_list)
    return "True"
