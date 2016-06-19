from flask import g

from app.models.session import session
from app.models.model import Users
from flask_httpauth import HTTPTokenAuth

auth = HTTPTokenAuth(scheme='Token')


@auth.verify_token
def basic_authentication(username_or_token):
    user = Users.verify_auth_token(username_or_token, session=session)
    if not user:
        user = session.query(Users).filter(Users.name == username_or_token).one_or_none()
        # if not user or not user.verify_password(password):
        #    return False
        if not user:
            return False
    g.user = user
    return True
