from app.routes.login_routes import UserLogin, UserLogout
from app.routes.user_routes import UsersMultipleRoute, UsersSingleRoute


def map_user_routes(api):
    api.add_resource(UsersMultipleRoute, '/users/')
    api.add_resource(UsersSingleRoute, '/users/<user_id>/')


def map_login_route(api):
    api.add_resource(UserLogin, '/login/')
    api.add_resource(UserLogout, '/logout/')
