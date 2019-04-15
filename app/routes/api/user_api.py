from flask import Blueprint, jsonify, Response, request
from flask import current_app as app
from bson import json_util
import json
from app import mongo
from app.models.User import User
from app.Messages import Messages
import re
import app.routes.api.wrappers as wrap


api_blueprint = Blueprint("user_api", __name__)


@api_blueprint.route("/user", methods=["GET", "POST"])
@wrap.require_login_token
def api_my_info(*args, **kwargs):
    print(kwargs["token"])
    return "OK"


@api_blueprint.route("/logout", methods=["GET", "POST"])
@wrap.require_login_token
def api_logout(*args, **kwargs):
    return_data = dict(Messages.message_logout)
    resp = jsonify(return_data)
    resp.set_cookie("token", "", expires=0)
    resp.status_code = 200
    return resp
