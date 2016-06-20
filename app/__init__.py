# -*- coding: utf-8 -*-

from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from app.factory import create_app

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


# def recreate_db(db):
#     db.drop_all()
#     db.create_all()


app = create_app(__name__, 'config')
# app.config.from_envvar('DIFFLY_SETTINGS', silent=True)
app.config['TRAP_HTTP_EXCEPTIONS'] = True

db = SQLAlchemy(app)
api = Api(app, catch_all_404s=True)

from app.routes import routes

# TODO: Remove when database migrations are in place.
db.drop_all()
db.create_all()

routes.map_login_route(api)
routes.map_user_routes(api)
