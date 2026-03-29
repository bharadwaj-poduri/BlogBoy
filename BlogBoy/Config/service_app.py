from flask import Flask

from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from Config.Settings import setup_config_logger


from datetime import timedelta
app = Flask(__name__)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

setup_config_logger(app)
api = Api(app)
app.secret_key = "any random string"

db = SQLAlchemy(app)
jwt = JWTManager(app)


from UMS.url_defs import *
from UMS.models import *
from Blogs.models import *
from Blogs.url_defs import *


@app.route('/')
def home():
    return {"message": "BlogBoy API is running"}, 200


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)