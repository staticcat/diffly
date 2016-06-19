import hashlib
import hmac
import json
import os
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature
from sqlalchemy.ext.hybrid import hybrid_property
from app import db

# TODO: Would prefer to use GUIDs for keys in all tables. Stop collisions across instances, also stop information leak
# TODO: Validate user email with validate_email
# TODO: Need to link users into text and comparisons for basic security.


class Users(db.Model):
    """Represents a user of the system. The user is linked to objects that they own and can view.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    email = db.Column(db.String(250), unique=True)
    _password = db.Column(db.LargeBinary(128))
    _salt = db.Column(db.String(128))

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        # When a user is first created, give them a salt
        if self._salt is None:
            self._salt = os.urandom(128)
        self._password = self._hash_password(value)

    def is_valid_password(self, password):
        new_hash = self._hash_password(password)
        return hmac.compare_digest(new_hash, self._password)

    def _hash_password(self, password):
        pwd = password.encode("utf-8")
        salt = bytes(self._salt)
        buff = hashlib.pbkdf2_hmac("sha512", pwd, salt, iterations=100000)
        return bytes(buff)

    # def verify_password(self, password):
    #     return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        from app import app
        s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    # def __repr__(self):
    #    return "<User #{:d}>".format(self.id)

    def as_dict(self):
        user_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        user_dict.pop('_password')
        user_dict.pop('_salt')
        return user_dict

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    @staticmethod
    def verify_auth_token(token, session):
        from app import app
        s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'], expires_in=600)
        try:
            data = s.loads(token)
        # valid token, but expired
        except SignatureExpired:
            return None
        # invalid token
        except BadSignature:
            return None
        user = session.query(Users).filter_by(Users.id == data['id']).count() > 0
        # user = session. Users.query.get(data['id'])
        return user


class ComparisonTexts(db.Model):
    """Text to compare is represented as a list of lines. This allows more fine grained control over number of
    lines returned.
    """
    __tablename__ = 'texts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TextLine(db.Model):
    """Lines that are compared. These belong to a text to compare.
    """
    __tablename__ = 'text_lines'

    id = db.Column(db.Integer, primary_key=True)
    line = db.Column(db.String(250))
    line_no = db.Column(db.Integer)
    text_to_compare_id = db.Column(db.Integer, db.ForeignKey('texts.id'))
    text_to_compare = db.relationship(ComparisonTexts)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TwoWayDiffs(db.Model):
    """A representation of the difference check performed on two pieces of text.
    """
    __tablename__ = 'two_way_diffs'

    id = db.Column(db.Integer, primary_key=True)
    left_text_id = db.Column(db.Integer, db.ForeignKey('texts.id'))
    right_text_id = db.Column(db.Integer, db.ForeignKey('texts.id'))
    left_text = db.relationship(ComparisonTexts, foreign_keys=[left_text_id])
    right_text = db.relationship(ComparisonTexts, foreign_keys=[right_text_id])

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class DiffOpCodes(db.Model):
    """The operation codes to perform to get the left text looking like the right.
    """
    __tablename__ = 'diff_op_codes'

    id = db.Column(db.Integer, primary_key=True)
    line_no = db.Column(db.Integer)
    op_code_tag = db.Column(db.String(6))
    left_text_start = db.Column(db.Integer)
    left_text_end = db.Column(db.Integer)
    right_text_start = db.Column(db.Integer)
    right_text_end = db.Column(db.Integer)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
