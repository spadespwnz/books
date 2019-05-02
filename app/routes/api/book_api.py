from flask import Blueprint, jsonify, Response, request
from flask import current_app as app
from bson import json_util, ObjectId
import json
from app import mongo
from app.Messages import Messages
import app.routes.api.wrappers as wrap

api_blueprint = Blueprint("book_api", __name__)

@api_blueprint.route("/to_read_list/add", methods=["POST"])
@wrap.require_login_token
def api_add_to_read_list(*args, **kwargs):
    '''
    Need to make responses
    '''
    username = kwargs["username"]
    req_data = request.get_json()
    book_id_raw = req_data.get("id")
    book_oid = ObjectId(book_id_raw)
    validId = verifyBookId(book_oid)
    if validId:
        update = mongo.db.users.update({"username":username},{"$addToSet":{"to_read_list":book_oid}})
        print(update)
    return "True"
def verifyBookId(id):
    book = mongo.db.editions.find_one({"_id":id})
    if (book):
        return True
    return False
