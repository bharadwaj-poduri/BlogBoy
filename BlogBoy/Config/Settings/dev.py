import os
from Config.Settings.base import BaseConfig

class Config(BaseConfig):
    DEBUG = True

    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:hanu1729@localhost/blogboy'
    SQLALCHEMY_POOL_RECYCLE = 100
