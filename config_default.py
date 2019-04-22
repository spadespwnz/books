class Config(object):
    DEBUG = False
    TESTING = False
    VERSION = "0.0.1"
    MODE = "UNSET"

class ProdConfig(Config):
    MODE = "PROD"
    pass

class DevConfig(Config):
    MODE = "DEV"
    DEBUG = True
    MONGO_URI='mongodb://localhost:27017/book_db'


class TestConfig(Config):
    MODE = "TEST"
    TESTING = True
