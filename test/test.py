# -*- coding: utf-8 -*-
"""
    Diffly Tests
    ~~~~~~~~~~~~
    Tests the Diffly application.
    :copyright:
    :license: BSD, see LICENSE for more details.
"""
import pytest
from app import db as _db
from factory import create_app
from flask import json
from model import Users

TEST_DATABASE_URI = 'sqlite:///'


@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    settings_override = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': TEST_DATABASE_URI
    }
    app = create_app(__name__, settings_override)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""
    _db.app = app
    _db.create_all()
    yield _db
    _db.drop_all()


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope='function')
def client(app):
    app.config['TESTING'] = True
    test_client = app.test_client()
    return test_client


# @pytest.fixture
# def client(request):
#     db_fd, app.config['DATABASE'] = tempfile.mkstemp()
#     app.config['TESTING'] = True
#     test_client = app.test_client()
#
#     with app.app_context():
#         init_db(engine=None)
#
#     def setup():
#
#
#     def teardown():
#         os.close(db_fd)
#         os.unlink(app.config['DATABASE'])
#
#     request.addfinalizer(teardown)
#
#     return test_client


def assert_is_json_content(rv, status_code):
    # noinspection PyUnusedLocal
    __tracebackhide__ = True
    assert rv.content_type == 'application/json'
    assert rv.status_code == status_code


def test_user_schema1(session):
    person_name = 'flake'
    uu = Users(name=person_name)
    session.add(uu)
    session.commit()

    assert uu.id == 1
    assert uu.name == person_name


def test_user_schema2(session):
    person_name = 'blake'
    uu = Users(name=person_name)
    session.add(uu)
    session.commit()

    assert uu.id == 1
    assert uu.name == person_name


# noinspection PyShadowingNames
def test_root_route_returns_404(client):
    rv = client.get('/')
    assert rv.status_code == 404


# noinspection PyShadowingNames
def test_empty_db_returns_no_users(client):
    """Views handle zero users in the database"""
    rv = client.get('/users/')

    assert_is_json_content(rv, 200)
    json_response = json.loads(rv.get_data())
    assert json_response['users'] == []


# noinspection PyShadowingNames
def test_post_user_returns_new_user(client):
    rv = client.post('/users/',
                     data={'name': 'joe', 'email': 'joe@jones.com'})
    assert_is_json_content(rv, 201)
    json_response = json.loads(rv.get_data())
    assert json_response['users']['name'] == 'joe'
    assert json_response['users']['email'] == 'joe@jones.com'


# noinspection PyShadowingNames
def test_get_user_returns_user_in_db(client):
    user_name = 'joe'
    user_email = 'joe@jones.com'
    user_password = 'password'
    user = Users(name=user_name, email=user_email, password=user_password)
    session.Add(user)
    rv = client.get('/users/')
    assert_is_json_content(rv, 200)
    json_response = json.loads(rv.get_data())
    assert json_response['users']

# ComparisonTexts
# TextLine
# TwoWayDiffs
# DiffOpCodes
