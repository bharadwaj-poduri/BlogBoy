from flask_restful import Resource, reqparse
import json
from Config.service_app import app
from UMS.models import Users, RevokedTokenModel
from flask import session
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from BlogBoy.resources import BaseResource

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)


class UserRegistration(BaseResource):
    def post(self):
        data = parser.parse_args()

        if Users.find_by_username(data['username']):
            error_message = 'User {} already exists'.format(data['username'])
            return self.json_response(success=False, error_message=error_message, error_code=400)

        new_user = Users(
            username=data['username'],
            password=Users.generate_hash(data['password'])
        )
        try:
            new_user.save_to_db()
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            body = {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            return self.json_response(success=True, error_code=200, data=body)
        except Exception:
            return self.json_response(success=False, error_message='Something went wrong', error_code=500)


class UserLogin(BaseResource):
    def post(self):
        data = parser.parse_args()
        current_user = Users.find_by_username(data['username'])

        if not current_user:
            error_message = 'User {} doesn\'t exist'.format(data['username'])
            return self.json_response(success=False, error_message= error_message, error_code=400)

        session['user_id'] = current_user.id
        session['username'] = current_user.username

        if Users.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            app.logger.info("Logged in as {}".format(current_user.username))
            body = {'message': 'Logged in as {}'.format(current_user.username),
                    'access_token': access_token,
                    'refresh_token': refresh_token
                    }
            return self.json_response(success=True, error_code=200, data=body)
        else:
            return self.json_response(success=False, error_message='Wrong credentials', error_code=400)


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            session.pop('user_id', None)
            session.pop('username', None)
            body = {
                'message': 'Access token has been revoked'
            }
            return self.json_response(success=True, error_code=200, data=body)
        except:
            return self.json_response(success=False, error_message='Something went wrong', error_code=500)


"""
Both UserLogoutAccess and UserLogoutRefresh have to be used combinedly to logout
"""


class UserLogoutRefresh(BaseResource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            body = {
                'message': 'Refresh token has been revoked'
            }
            return self.json_response(success=True, error_code=200, data=body)
        except:
            return self.json_response(success=False, error_message='Something went wrong', error_code=500)


"""
TokenRefresh needs to called every 15 min
"""


class TokenRefresh(BaseResource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        body = {'access_token': access_token}
        return self.json_response(success=True, error_code=200, data=body)


class AllUsers(BaseResource):
    @jwt_required
    def get(self):
        return Users.return_all()

    @jwt_required
    def delete(self):
        return Users.delete_all()
