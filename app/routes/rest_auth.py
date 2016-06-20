from flask import g
from flask_httpauth import HTTPTokenAuth
from model import Users
from app import db

auth = HTTPTokenAuth(scheme='Token')

# TODO: Implement JWT as token type. Require unit testing to make this simpler to test
# jwt = JWT(app.config['SECRET_KEY'], expires_in=3600)


@auth.verify_token
def basic_authentication(token):
    # g.user = None
    # try:
    #     data = jwt.loads(token)
    # except:
    #     return False
    # if 'username' in data:
    #     g.user = data['username']
    #     return True
    # return False

    user = Users.verify_auth_token(token, session=db.session)
    if not user:
        user = db.session.query(Users).filter(Users.name == token).one_or_none()
        if not user:
            return False
    g.user = user
    return True
