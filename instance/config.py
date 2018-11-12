import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False


class Development(Config):
    """Configurations for Development."""
    DEBUG = True
    DB_URL = "dbname='storemanager' host='localhost' port='5432' user='postgres' password='Password12#'"



class Testing(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = True
    DB_URL = "dbname='storemanagertest' host='localhost' port='5432' user='postgres' password='Password12#'"

class Staging(Config):
    """Configurations for Staging."""
    DEBUG = True


class Production(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
    DB_URL = "postgres://enkpqtcmagriuy:0f421ed7d1810f57d38459c07ab9cbe4f0195e5e885666285c96bc4e82da14e5@ec2-174-129-212-12.compute-1.amazonaws.com:5432/d7mdvc21nohe4q"

config = {
    'development': Development,
    'testing': Testing,
    'staging': Staging,
    'production': Production,
    'db_url': "dbname='storemanager' host='localhost' port='5432' user='postgres' password='Password12#'",
    'test_db_url': "dbname='storemanagertest' host='localhost' port='5432' user='postgres' password='Password12#'"
}