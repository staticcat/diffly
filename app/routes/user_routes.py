from flask_restful import Resource, abort, reqparse
from app import db
from model import Users
from flask_sqlalchemy import Pagination
from rest_auth import auth


def val_user_name(value, name):
    if value is None:
        raise ValueError("The {} can not be blank.".format(name))
    return value


def val_user_email(value, name):
    if value is None:
        raise ValueError("The {} can not be blank.".format(name))
    return value


user_parser = reqparse.RequestParser()
user_parser.add_argument('name', type=val_user_name, trim=True, required=True)
user_parser.add_argument('email', type=val_user_email, trim=True, required=True)
user_parser.add_argument('password', trim=True, required=True)


def abort_user_doesnt_exist(user_id):
    abort(404, message="User with ID {} doesn't exist".format(user_id))


def abort_user_name_already_exists(user_name):
    abort(400, message="User with user name {} already exists".format(user_name))


def abort_user_not_unique():
    abort(400, message="User name or email already in use.")


class UsersMultipleRoute(Resource):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get():
        """

        :rtype:
        """
        # users = Users.query.paginate(1, 4, False).items
        # TODO: Implement pagination. Session query doesn't seem to support pagination
        users = db.session.query(Users).all()
        return {'users': users}

    @staticmethod
    def post():
        args = user_parser.parse_args()
        if not Users.email_is_unique(args['email'], None) or not Users.name_is_unique(args['name'], None):
            abort_user_not_unique()
        new_user = Users(name=args['name'], email=args['email'], password=args['password'])
        db.session.add(new_user)
        db.session.commit()
        return {'users': new_user.as_dict()}, 201


class UsersSingleRoute(Resource):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get(user_id):
        """

        :rtype:
        """
        users = db.session.query(Users).filter(Users.id == user_id).one_or_none()
        if not users:
            abort_user_doesnt_exist(user_id)
        return {'user': users.as_dict()}

    @staticmethod
    def put(user_id):
        user = db.session.query(Users).filter(Users.id == user_id).one_or_none()
        if not user:
            abort_user_doesnt_exist(user_id)
        args = user_parser.parse_args()
        if not Users.email_is_unique(args['email'], user_id) or not Users.name_is_unique(args['name'], user_id):
            abort_user_not_unique()
        user.name = args['name']
        user.email = args['email']
        user.password = args['password']
        db.session.add(user)
        db.session.commit()
        return {'user': user.as_dict()}
