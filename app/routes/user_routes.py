from flask_restful import Resource, abort,  reqparse

from app.models.model import Users
from app.models.session import session
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
user_parser.add_argument('name', type=val_user_name, required=True)
user_parser.add_argument('email', type=val_user_email, required=True)
user_parser.add_argument('password', trim=True, required=True)


def abort_user_doesnt_exist(user_id):
    abort(404, message="User with ID {} doesn't exist".format(user_id))


def abort_user_name_already_exists(user_name):
    abort(400, message="User with user name {} already exists".format(user_name))


class UsersMultipleRoute(Resource):
    def __init__(self):
        super().__init__()

    @staticmethod
    @auth.login_required
    def get():
        """

        :rtype:
        """
        users = session.query(Users).all()
        return {'users': users}

    @staticmethod
    def post():
        args = user_parser.parse_args()
        users_name_taken = session.query(Users).filter(Users.name == args['name']).count() > 0
        if users_name_taken:
            abort_user_name_already_exists(args['name'])
        new_user = Users(name=args['name'], email=args['email'], password=args['password'])
        session.add(new_user)
        session.commit()
        return {'users': new_user.as_dict()}, 201


class UsersSingleRoute(Resource):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get(user_id):
        """

        :rtype:
        """
        users = session.query(Users).filter(Users.id == user_id).one_or_none()
        if not users:
            abort_user_doesnt_exist(user_id)
        return {'users': users.as_dict()}
