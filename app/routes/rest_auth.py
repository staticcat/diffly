from flask import g

from app.diffly import auth, session
from models.model import Users


@auth.verify_token
def basic_authentication(username_or_token):
    user = Users.verify_auth_token(username_or_token, session=session)
    if not user:
        user = Users.query.filter_by(username=username_or_token).first()
        # if not user or not user.verify_password(password):
        #    return False
        if not user:
            return False
    g.user = user
    return True
