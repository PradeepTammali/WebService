# -*- coding: utf-8 -*-
from typing import Any

import pytest
from flask import Flask, Response
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer
from sqlalchemy_utils import drop_database

from omdb import app
from omdb.db.base import StringColumn, db
from omdb.db.model import Model
from omdb.db.query import BaseQueryList


class BaseTestModelQueryList(BaseQueryList['BaseTestModel']):
    pass


class BaseTestModel(Model):
    __tablename__ = 'test_model'
    querylist = BaseTestModelQueryList

    id = Column(Integer, primary_key=True)
    value = StringColumn()
    value2 = StringColumn()
    value3 = StringColumn()

    def __init__(self, value, value2, value3):
        super().__init__()

        self.value = value
        self.value2 = value2
        self.value3 = value3


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
    def setup_application(self, test_app: Flask):
        self._app = test_app

    @pytest.fixture(autouse=True)
    def init_db(self, test_app: Flask) -> SQLAlchemy:
        with test_app.app_context():
            yield db
            # TODO: Remove commit after it's handled in after_request
            db.session.commit()
            db.drop_all()
            drop_database(test_app.config.get('SQLALCHEMY_DATABASE_URI'))

    @property
    def client(self) -> BaseTestFlaskClient:
        return self._app.test_client()
