from flask import g
from flask_httpauth import HTTPTokenAuth
from model import Users
from app import db

auth = HTTPTokenAuth(scheme='Token')


@auth.verify_token
def basic_authentication(username_or_token):
    user = Users.verify_auth_token(username_or_token, session=db.session)
    if not user:
        user = db.session.query(Users).filter(Users.name == username_or_token).one_or_none()
        # if not user or not user.verify_password(password):
        #    return False
        if not user:
            return False
    g.user = user
    return True
