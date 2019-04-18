from flask import request, jsonify
from flask import current_app as app
from app import redis
from functools import wraps
from app.Messages import Messages
import jwt


def require_login_token(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        data = request.get_json()
        token = None
        if data:
            token = data.get("token")
        if request.cookies:
            token = request.cookies.get("token")
        if token == None:
            return_data = dict(Messages.error_invalid_token)
            resp = jsonify(return_data)
            resp.status_code = 200
            return resp

        # Token has been 'logged out'
        if redis.get(token) != None:
            return_data = dict(Messages.error_invalid_token)
            resp = jsonify(return_data)
            resp.status_code = 200
            return resp

        try:
            data = jwt.decode(token, app.jwt_key)
        except (ValueError, jwt.exceptions.DecodeError, jwt.ExpiredSignatureError):
            return_data = dict(Messages.error_invalid_token)
            resp = jsonify(return_data)
            resp.status_code = 200
            return resp

        kwargs["username"] = data["username"]
        kwargs["token"] = token
        kwargs["token_expire"] = data["exp"]
        return func(*args, **kwargs)

    return check_token
