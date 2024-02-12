# -*- coding: utf-8 -*-
from typing import Any
from unittest import TestCase

import pytest
from flask import Flask, Response
from flask_login import FlaskLoginClient, login_user
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import close_all_sessions
from sqlalchemy_utils import database_exists, drop_database

from omdb import app
from omdb.config import config
from omdb.db.base import db
from omdb.models.user import User
from omdb.utils.hashers import generate_email, random_hash16, random_hash32
from tests.shared.http import http_blueprint
from tests.shared.request_hooks import request_hooks_blueprint


class BaseTestFlaskClient(FlaskLoginClient):
    def json_post(self, url: str, **kwargs: Any) -> Response:
        kwargs['content_type'] = 'application/json'
        return self.post(url, **kwargs)

    def json_put(self, url: str, **kwargs: Any) -> Response:
        kwargs['content_type'] = 'application/json'
        return self.put(url, **kwargs)

    def json_delete(self, url: str, **kwargs: Any) -> Response:
        kwargs['content_type'] = 'application/json'
        return self.delete(url, **kwargs)


class BaseTest:
    _app: Flask
    assert_raises = staticmethod(pytest.raises)
    assert_equal = staticmethod(TestCase().assertEqual)
    assert_in = staticmethod(TestCase().assertIn)
    assert_not_in = staticmethod(TestCase().assertNotIn)

    @pytest.fixture(autouse=True)
    def test_db(self, worker_id):
        db_url = make_url(config.SQLALCHEMY_DATABASE_URI)
        db_url = db_url.set(database=f'{config.MYSQL_DEFAULT_DB_NAME}_{worker_id}_{random_hash32()}')
        config.SQLALCHEMY_DATABASE_URI = db_url.render_as_string(hide_password=False)

    @pytest.fixture
    def test_app(self, test_db) -> Flask:  # pylint: disable=unused-argument
        application = app.create_app('test')
        application.test_client_class = BaseTestFlaskClient

        # Register test blueprints
        application.register_blueprint(request_hooks_blueprint)
        application.register_blueprint(http_blueprint)
        return application

    @pytest.fixture(autouse=True)
    def setup_application(self, test_app: Flask):
        self._app = test_app

    @pytest.fixture(autouse=True)
    def init_db(self, test_app: Flask):
        with test_app.app_context():
            yield db
            db.session.rollback()
            db.drop_all()
            close_all_sessions()
            if database_exists(test_app.config.get('SQLALCHEMY_DATABASE_URI')):
                drop_database(test_app.config.get('SQLALCHEMY_DATABASE_URI'))

    @property
    def client(self) -> BaseTestFlaskClient:
        return self._app.test_client()

    def login_as_admin(self) -> User | None:
        admin_user: User | None = User.one_or_none(email=config.DEFAULT_USER_EMAIL)
        if admin_user is None:
            admin_user = User(email=config.DEFAULT_USER_EMAIL, password=config.DEFAULT_USER_PASSWORD, is_admin=True)
            admin_user.save()
        with self._app.test_request_context():
            login_user(user=admin_user)
        return admin_user

    def login_as_user(self) -> User | None:
        email: str = generate_email()
        password: str = random_hash16()
        user: User | None = User.one_or_none(email=email)
        if user is None:
            user = User(email=email, password=password)
            user.save()
        with self._app.test_request_context():
            login_user(user=user)
        return user
