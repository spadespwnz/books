from flask import request, jsonify
from functools import wraps
from app.Messages import Messages


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
            print("Invalid Token")
            return_data = dict(Messages.error_invalid_token)
            resp = jsonify(return_data)
            resp.status_code = 200
            return resp

        kwargs["token"] = token
        return func(*args, **kwargs)

    return check_token
