import hashlib
import hmac
import json
from random import SystemRandom
from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

Base = declarative_base()


# TODO: Would prefer to use GUIDs for keys in all tables. Stop collisions across instances, also stop information leak
# TODO: Validate user email with validate_email
# TODO: Need to link users into text and comparisons for basic security.


class Users(Base):
    """Represents a user of the system. The user is linked to objects that they own and can view.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    email = Column(String(250), unique=True)
    _password = Column(LargeBinary(120))
    _salt = Column(String(120))

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        # When a user is first created, give them a salt
        if self._salt is None:
            self._salt = bytes(SystemRandom().getrandbits(128))
        self._password = self._hash_password(value)

    def is_valid_password(self, password):
        new_hash = self._hash_password(password)
        return hmac.compare_digest(new_hash, self._password)

    def _hash_password(self, password):
        pwd = password.encode("utf-8")
        salt = bytes(self._salt)
        buff = hashlib.pbkdf2_hmac("sha512", pwd, salt, iterations=100000)
        return bytes(buff)

    def __repr__(self):
        return "<User #{:d}>".format(self.id)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class ComparisonTexts(Base):
    """Text to compare is represented as a list of lines. This allows more fine grained control over number of
    lines returned.
    """
    __tablename__ = 'texts'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TextLine(Base):
    """Lines that are compared. These belong to a text to compare.
    """
    __tablename__ = 'text_lines'

    id = Column(Integer, primary_key=True)
    line = Column(String(250))
    line_no = Column(Integer)
    text_to_compare_id = Column(Integer, ForeignKey('texts.id'))
    text_to_compare = relationship(ComparisonTexts)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TwoWayDiffs(Base):
    """A representation of the difference check performed on two pieces of text.
    """
    __tablename__ = 'two_way_diffs'

    id = Column(Integer, primary_key=True)
    left_text_id = Column(Integer, ForeignKey('texts.id'))
    right_text_id = Column(Integer, ForeignKey('texts.id'))
    left_text = relationship(ComparisonTexts, foreign_keys=[left_text_id])
    right_text = relationship(ComparisonTexts, foreign_keys=[right_text_id])

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class DiffOpCodes(Base):
    """The operation codes to perform to get the left text looking like the right.
    """
    __tablename__ = 'diff_op_codes'

    id = Column(Integer, primary_key=True)
    line_no = Column(Integer)
    op_code_tag = Column(String(6))
    left_text_start = Column(Integer)
    left_text_end = Column(Integer)
    right_text_start = Column(Integer)
    right_text_end = Column(Integer)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
