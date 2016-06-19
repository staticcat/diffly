from flask_sqlalchemy_session import flask_scoped_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from consts import database_dir

engine = create_engine("sqlite:///" + database_dir)

session_factory = sessionmaker(bind=engine)
session = flask_scoped_session(session_factory)