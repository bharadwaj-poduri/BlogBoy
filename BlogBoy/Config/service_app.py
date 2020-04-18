from flask import Flask

from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine


app = Flask(__name__)

api = Api(app)
app.secret_key = "any random string"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres@localhost/blogboy'
app.config["SQLALCHEMY_POOL_RECYCLE"] = 100

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
#engine = create_engine(app.config.get('SQLALCHEMY_DATABASE_URI'))

db = SQLAlchemy(app)
jwt = JWTManager(app)


from UMS.url_defs import *
from UMS.models import *
from Blogs.models import *
from Blogs.url_defs import *

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)