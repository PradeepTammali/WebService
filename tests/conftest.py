# -*- coding: utf-8 -*-
from typing import Any

import pytest
from flask import Flask, Response
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy

from omdb import app
from omdb.db.base import db


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

    @pytest.fixture
    def test_app(self) -> Flask:
        application = app.create_app('test')
        application.test_client_class = BaseTestFlaskClient

        return application

    @pytest.fixture(autouse=True)
    def setup_application(self, test_app: Flask) -> None:
        self._app = test_app

    @pytest.fixture(autouse=True)
    def init_db(self, test_app: Flask) -> SQLAlchemy:
        with test_app.app_context():
            db.create_all()
            yield db
            # TODO: Remove commit after it's handled in after_request
            db.session.commit()
            db.drop_all()

    @property
    def client(self) -> BaseTestFlaskClient:
        return self._app.test_client()
