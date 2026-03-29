import os

class BaseConfig(object):
    DEBUG = False

    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASS = os.environ.get('DB_PASS', 'hanu1729')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_NAME = os.environ.get('DB_NAME', 'blogboy')
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASS, DB_HOST, DB_NAME)
    SQLALCHEMY_POOL_RECYCLE = 100

    JWT_SECRET_KEY = 'jwt-secret-string'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

