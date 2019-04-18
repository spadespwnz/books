from flask import Blueprint, jsonify, Response, request
from flask import current_app as app
from bson import json_util
import json
from app import mongo
from app import redis
from app.models.User import User
from app.Messages import Messages
import re
import app.routes.api.wrappers as wrap


api_blueprint = Blueprint("user_api", __name__)


@api_blueprint.route("/check_token", methods=["GET", "POST"])
@wrap.require_login_token
def api_my_info(*args, **kwargs):
    return_data = dict(Messages.message_token_check)
    return_data["data"] = {"username": kwargs["username"]}
    resp = jsonify(return_data)
    resp.status_code = 200
    return resp


@api_blueprint.route("/logout", methods=["GET", "POST"])
@wrap.require_login_token
def api_logout(*args, **kwargs):
    redis.set(kwargs["token"], 1)
    redis.expireat(kwargs["token"], kwargs["token_expire"])
    return_data = dict(Messages.message_logout)
    resp = jsonify(return_data)
    resp.set_cookie("token", "", expires=0)
    resp.status_code = 200
    return resp
