class Messages:
    message_user_list = {"err": False, "msg": "Found User List", "code": 0}
    message_check_user_exists = {
        "err": False,
        "msg": "Checking User Existance",
        "code": 1,
    }
    message_check_email_exists = {
        "err": False,
        "msg": "Checking Email Existance",
        "code": 1.1,
    }
    message_valid_username = {"err": False, "msg": "Checking Username Valid", "code": 2}
    message_valid_email = {"err": False, "msg": "Checking Email Valid", "code": 2.1}
    message_register = {"err": False, "msg": "Registering Account", "code": 3}
    message_logout = {"err": False, "msg": "Logging out", "code": 4}
    message_login = {"err": False, "msg": "Logging In", "code": 5}
    message_login_fail = {"err": False, "msg": "Invalid Login Credentials", "code": 5.1}
    message_token_check = {"err": False, "msg": "Checking Login Token", "code": 6}

    error_invalid_token = {"err": True, "msg": "Invalid Token", "code": 2000}
