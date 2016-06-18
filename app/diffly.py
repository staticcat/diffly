# -*- coding: utf-8 -*-
import os

from flask import Flask, Response, request, session, jsonify
from flask_restful import Resource, Api, abort, reqparse
from flask_sqlalchemy_session import flask_scoped_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.model import Base, Users

# TODO: Move routes to route module
# TODO: Move views to view_* modules
# TODO: Implement database migration with alembic
# TODO: Figure out flask versioning.
# TODO: Figure out pytest for testing flask and database
# TODO: Figure out session logic for database
# TODO: CompareText get list, get single, post and delete
# TODO: User get list, get single, post and delete
# TODO: TwoWayDiff get list, get single, post and delete
# TODO: Look at using Flask-Restless for rest resource classes

# TODO: 201 created - created a new resource
# TODO: 202 accepted - successfully set the request to perform long running task
# TODO: 304 not modified - performed a conditional GET request and access is allowed, but nothing was done.
# TODO: 400 bad request - could not understand request
# TODO: 401 not auth - does not correct auth for action
# TODO: 403 forbidden - although authed, not allowed to perform action
# TODO: 404 not found - not found anything matching the Request-URI.
# TODO: 500 internal server error -

basedir = os.path.realpath(os.path.dirname(__file__))
database_dir = os.path.join(basedir, "db", "diffly.db")
engine = create_engine("sqlite:///" + database_dir)


session_factory = sessionmaker(bind=engine)
app = Flask(__name__)
api = Api(app, catch_all_404s=True)

app.config.update(dict(
    DATABASE=database_dir,
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
#app.config.from_envvar('DIFFLY_SETTINGS', silent=True)
app.config['TRAP_HTTP_EXCEPTIONS'] = True

scoped_sess = flask_scoped_session(session_factory, app)
session = session_factory()


def user_name(value, name):
    if value is None:
        raise ValueError("The user name can not be blank.")
    return value


def user_email(value, name):
    if value is None:
        raise ValueError("The user email can not be blank.")
    return value

user_parser = reqparse.RequestParser()
user_parser.add_argument('name', type=user_name)
user_parser.add_argument('email', type=user_email)


def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def abort_user_doesnt_exist(user_id):
    abort(404, message="User with ID {} doesn't exist".format(user_id))


class UsersMultipleRoute(Resource):
    def get(self):
        """

        :rtype:
        """
        users = session.query(Users).all()
        return {'users': users}

    def post(self):
        args = user_parser.parse_args()
        new_user = Users(name=args['name'], email=args['email'])
        session.add(new_user)
        session.commit()
        return {'users': new_user.as_dict()}, 201


class UsersSingleRoute(Resource):
    def get(self, user_id):
        """

        :rtype:
        """
        users = session.query(Users).filter(Users.id == user_id).one_or_none()
        if not users:
            abort_user_doesnt_exist(user_id)
        return {'users': users}


api.add_resource(UsersMultipleRoute, '/users/')
api.add_resource(UsersSingleRoute, '/users/<user_id>/')

if __name__ == '__main__':
    init_db()
    app.run()
