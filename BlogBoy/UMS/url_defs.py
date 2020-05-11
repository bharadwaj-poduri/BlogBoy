from Config.service_app import api

from UMS.resources import UserRegistration, UserLogin, UserLogoutAccess, TokenRefresh, AllUsers, UserLogoutRefresh


api.add_resource(UserRegistration, '/registration')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogoutAccess, '/logout/access')
api.add_resource(UserLogoutRefresh, '/logout/refresh')
api.add_resource(TokenRefresh, '/token/refresh')
api.add_resource(AllUsers, '/users')
