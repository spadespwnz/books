from flask import request
from functools import wraps
def require_login_token(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        data = requests.get_json()
        token = data.get("token")
        kwargs['token'] = token

        # If token is bad, return error, else return user




        return func(*args, **kwargs)

    return check_token
