# -*- coding: utf-8 -*-
"""
    Diffly Tests
    ~~~~~~~~~~~~
    Tests the Diffly application.
    :copyright:
    :license: BSD, see LICENSE for more details.
"""

import pytest
import os
import tempfile
from flask import json
from app.diffly import app, init_db


@pytest.fixture
def client(request):
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    test_client = app.test_client()

    with app.app_context():
        init_db()

    def teardown():
        os.close(db_fd)
        os.unlink(app.config['DATABASE'])

    request.addfinalizer(teardown)

    return test_client


def assert_is_json_content(rv, status_code):
    __tracebackhide__ = True
    assert rv.content_type == 'application/json'
    assert rv.status_code == status_code


def test_root_route_returns_404(client):
    rv = client.get('/')
    assert rv.status_code == 404


def test_empty_db_returns_no_users(client):
    """Views handle zero users in the database"""
    rv = client.get('/users/')

    assert_is_json_content(rv, 200)
    json_response = json.loads(rv.get_data())
    assert json_response['users'] == []


def test_post_user_returns_new_user(client):
    rv = client.post('/users/',
                     data={'name': 'joe', 'email': 'joe@joes.com'})
    assert_is_json_content(rv, 201)
    json_response = json.loads(rv.get_data())
    assert json_response['users']['name'] == 'joe'
    assert json_response['users']['email'] == 'joe@joes.com'



# ComparisonTexts
# TextLine
# TwoWayDiffs
# DiffOpCodes