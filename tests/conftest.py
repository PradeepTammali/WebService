# -*- coding: utf-8 -*-
from typing import Any

import pytest
from flask import Flask, Response
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import close_all_sessions
from sqlalchemy_utils import database_exists, drop_database

from omdb import app
from omdb.db.base import db
from tests.shared.http import http_blueprint


class BaseTestFlaskClient(FlaskClient):
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

    @pytest.fixture
    def test_app(self) -> Flask:
        application = app.create_app('test')
        application.test_client_class = BaseTestFlaskClient

        # Register test blueprints
        application.register_blueprint(http_blueprint)
        return application

    @pytest.fixture(autouse=True)
    def setup_application(self, test_app: Flask):
        self._app = test_app

    @pytest.fixture(autouse=True)
    def init_db(self, test_app: Flask) -> SQLAlchemy:
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
