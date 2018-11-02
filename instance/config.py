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
    DB_URL = "postgres://uiucbnlliwkcmi:adc815dab4a8e7a71ca743d991376069d1358f224bb33658631a0099d3732f3a@ec2-75-101-138-26.compute-1.amazonaws.com:5432/d3a20o9lhegqmt"

config = {
    'development': Development,
    'testing': Testing,
    'staging': Staging,
    'production': Production,
    'db_url': "dbname='storemanager' host='localhost' port='5432' user='postgres' password='Password12#'",
    'test_db_url': "dbname='storemanagertest' host='localhost' port='5432' user='postgres' password='Password12#'"
}