# -*- coding: utf-8 -*-
from flask_httpauth import HTTPTokenAuth
from flask_restful import Api

from app.consts import database_dir
from app.factory import create_app
from app.models.session import session, engine
from app.models.model import init_db
from app.routes import routes

# TODO: __LONG TERM__
# TODO: Implement database migration with alembic

# TODO: __SHORT TERM__
# TODO: Figure out flask versioning.
# TODO: CompareText get list, get single, post and delete
# TODO: User get list, get single, post and delete
# TODO: TwoWayDiff get list, get single, post and delete

# TODO: 201 created - created a new resource
# TODO: 202 accepted - successfully set the request to perform long running task
# TODO: 304 not modified - performed a conditional GET request and access is allowed, but nothing was done.
# TODO: 400 bad request - could not understand request
# TODO: 401 not auth - does not correct auth for action
# TODO: 403 forbidden - although authed, not allowed to perform action
# TODO: 404 not found - not found anything matching the Request-URI.
# TODO: 500 internal server error -


app = create_app(None)
api = Api(app, catch_all_404s=True)
auth = HTTPTokenAuth(scheme='Token')

app.config.update(dict(
    DATABASE=database_dir,
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
# app.config.from_envvar('DIFFLY_SETTINGS', silent=True)
app.config['TRAP_HTTP_EXCEPTIONS'] = True


session.init_app(app=app)

routes.map_login_route(api)
routes.map_user_routes(api)

if __name__ == '__main__':
    init_db(engine=engine)
    app.run()
