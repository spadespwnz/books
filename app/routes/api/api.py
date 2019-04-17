from flask import Blueprint, jsonify, Response, request
from flask import current_app as app
from bson import json_util
import jwt
import json
from app import mongo

from app.models.User import User
from app.Messages import Messages
import re

api_blueprint = Blueprint("user_login_api", __name__)


@api_blueprint.route("/", methods=["GET"])
def api():
    for doc in mongo.db.books.find():
        print(doc)
        return_data = {"api_version": app.config.get("VERSION")}
    resp = jsonify(return_data)
    resp.status_code = 200

    return resp


@api_blueprint.route("/test", methods=["GET"])
def api_test():
    return_data = {"test": "wtf", "somenum": 8}
    resp = jsonify(return_data)
    resp.status_code = 200

    return resp


@api_blueprint.route("/login", methods=["POST"])
def api_login():
    req_data = request.get_json()
    username = req_data.get("email_or_username")
    email = req_data.get("email_or_username")
    password = req_data.get("password")
    user = User(mongo.db, username=username, email=email, password=password)
    validCreds = user.verify()
    if not validCreds:
        return_data = dict(Messages.message_login_fail)
        resp = jsonify(return_data)
        resp.status_code = 200
        return resp

    return sendToken(user, dict(Messages.message_login))


@api_blueprint.route("/register", methods=["POST"])
def api_register():
    req_data = request.get_json()
    username = req_data.get("username")
    email = req_data.get("email")
    password = req_data.get("password")
    return_data = dict(Messages.message_register)

    if valid_email_string(email) == False:
        return_data["data"] = False
        return_data["reason"] = "Invalid Email"
        resp = jsonify(return_data)
        resp.status_code = 200
        return resp

    if valid_username_string(username) == False:
        return_data["data"] = False
        return_data["reason"] = "Invalid Username"
        resp = jsonify(return_data)
        resp.status_code = 200
        return resp

    if valid_password_string(password) == False:
        return_data["data"] = False
        return_data["reason"] = "Invalid Password"
        resp = jsonify(return_data)
        resp.status_code = 200
        return resp

    user = User(mongo.db, username=username, email=email, password=password)
    created = user.create()
    if created == False:
        return_data["data"] = False
        return_data["reason"] = "User Already Exists"
        resp = jsonify(return_data)
        resp.status_code = 200
        return resp

    """
    userListCursor = User.get_all(mongo.db)
    for doc in userList:
        print(doc)
    return_data = Messages.message_user_list
    userList = [json.dumps(doc, default=json_util.default) for doc in userListCursor]
    """
    # userList_string= dumps(userList)
    return sendToken(user, return_data)


# Returns True only if the email is not in the Database
@api_blueprint.route("/check_email_exist", methods=["POST"])
def api_check_email_exist():
    req_data = request.get_json()
    email = req_data.get("email")
    exists = User.exists(mongo.db, {"email": email})
    return_data = dict(Messages.message_check_email_exists)
    return_data["data"] = exists
    # user = User(mongo.db, username = username)
    # print(user.verify())
    resp = jsonify(return_data)
    resp.status_code = 200
    return resp


# Returns True only when the email is valid, and not in the Database
@api_blueprint.route("/check_valid_email", methods=["POST"])
def api_check_valid_email():
    req_data = request.get_json()
    email = req_data.get("email")
    exists = User.exists(mongo.db, {"email": email})
    if exists:
        return_data = dict(Messages.message_valid_email)
        return_data["reason"] = "Email Already Exists."
        return_data["data"] = not exists
        resp = jsonify(return_data)
        resp.status_code = 200
        return resp
    if valid_email_string(email) != True:
        return_data = dict(Messages.message_valid_email)
        return_data["reason"] = "Invalid Email"
        return_data["data"] = False
        resp = jsonify(return_data)
        resp.status_code = 200
        return resp
    return_data = dict(Messages.message_valid_email)
    return_data["data"] = True

    resp = jsonify(return_data)
    resp.status_code = 200
    return resp


# Returns True only if the username is not in the Database
@api_blueprint.route("/check_username_exist", methods=["POST"])
def api_check_user_exist():
    req_data = request.get_json()
    username = req_data.get("username")
    exists = User.exists(mongo.db, {"username": username})
    return_data = dict(Messages.message_check_user_exists)
    return_data["data"] = exists
    # user = User(mongo.db, username = username)
    # print(user.verify())
    resp = jsonify(return_data)
    resp.status_code = 200
    return resp


# Returns True only when the username is valid, and not in the Database
@api_blueprint.route("/check_valid_username", methods=["POST"])
def api_check_valid_username():
    req_data = request.get_json()
    username = req_data.get("username")
    exists = User.exists(mongo.db, {"username": username})
    if exists:
        return_data = dict(Messages.message_valid_username)
        return_data["reason"] = "Username Already Exists."
        return_data["data"] = not exists
        resp = jsonify(return_data)
        resp.status_code = 200
        return resp
    if valid_username_string(username) != True:
        return_data = dict(Messages.message_valid_username)
        return_data["reason"] = "Invalid Username"
        return_data["data"] = False
        resp = jsonify(return_data)
        resp.status_code = 200
        return resp
    return_data = dict(Messages.message_valid_username)
    return_data["data"] = True

    resp = jsonify(return_data)
    resp.status_code = 200
    return resp


@api_blueprint.route("/drop", methods=["GET"])
def api_drop():
    print("DROPPING DB")
    mongo.db.users.drop()
    return "ok"


def valid_email_string(s):
    if s == None:
        return False
    result = re.search("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", s)
    if result == None:
        return False
    return True


def valid_username_string(s):
    if s == None:
        return False
    result = re.search("^[a-zA-Z0-9_]{3,20}$", s)
    if result == None:
        return False
    return True


def valid_password_string(s):
    if s == None:
        return False
    result = re.search("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", s)
    if result == None:
        return False
    return True


def sendToken(user, return_data):
    payload = {"username": user.username, "email": user.email}
    token = jwt.encode(payload, app.jwt_key).decode("utf-8")
    return_data["data"] = {"success": True, "token": token}
    resp = jsonify(return_data)
    resp.status_code = 200
    secure_cookie = False
    if app.config.get("MODE") == "PROD":
        secure_cookie = True
    resp.set_cookie("token", token, httponly=True, secure=secure_cookie)
    return resp
