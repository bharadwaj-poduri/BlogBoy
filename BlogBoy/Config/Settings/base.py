class BaseConfig(object):
    DEBUG = False

    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:hanu1729@localhost/blogboy'
    SQLALCHEMY_POOL_RECYCLE = 100
