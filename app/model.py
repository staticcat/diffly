from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# TODO: Would prefer to use GUIDs for keys in all tables. Stop collisions across instances, also stop information leak
# TODO: Validate user email with validate_email
# TODO: Need to link users into text and comparisons for basic security.


class User(Base):
    """Represents a user of the system. The user is linked to objects that they own and can view.
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    email = Column(String(250), unique=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class CompareText(Base):
    """Text to compare is represented as a list of lines. This allows more fine grained control over number of
    lines returned.
    """
    __tablename__ = 'text'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TextLine(Base):
    """Lines that are compared. These belong to a text to compare.
    """
    __tablename__ = 'text_line'

    id = Column(Integer, primary_key=True)
    line = Column(String(250))
    line_no = Column(Integer)
    text_to_compare_id = Column(Integer, ForeignKey('text.id'))
    text_to_compare = relationship(CompareText)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TwoWayDiff(Base):
    """A representation of the difference check performed on two pieces of text.
    """
    __tablename__ = 'two_way_diff'

    id = Column(Integer, primary_key=True)
    left_text_id = Column(Integer, ForeignKey('text.id'))
    right_text_id = Column(Integer, ForeignKey('text.id'))
    left_text = relationship(CompareText, foreign_keys=[left_text_id])
    right_text = relationship(CompareText, foreign_keys=[right_text_id])

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
