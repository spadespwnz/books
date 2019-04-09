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

class TestConfig(Config):
    MODE = "TEST"
    TESTING = True
