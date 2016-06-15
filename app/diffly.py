import os
from flask import Flask, jsonify
from flask_sqlalchemy_session import flask_scoped_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.model import Base, User

# TODO: Move routes to route module
# TODO: Move views to view_* modules
# TODO: Implement database migration with alembic
# TODO: Figure out flask versioning.
# TODO: Figure out pytest for testing flask and database
# TODO: Figure out session logic for database

basedir = os.path.realpath(os.path.dirname(__file__))
databasedir = os.path.join(basedir, "db", "diffly.db")
engine = create_engine("sqlite:///" + databasedir)


session_factory = sessionmaker(bind=engine)
app = Flask(__name__)

scoped_sess = flask_scoped_session(session_factory, app)
session = session_factory()

def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/users/', methods=['GET'])
def get_users():
    users = session.query(User).all()
    return jsonify({'users': users})


@app.route('/users/<int:id>/', methods=['GET'])
def get_user(id):
    users = session.query(User).filter(User.id == id).first()
    if not users:
        raise InvalidUsage('User not available.', status_code=404)
    return jsonify({'users': users})

if __name__ == '__main__':
    init_db()
    app.run()
