# -*- coding: utf-8 -*-
import datetime

import pytest
import pytz
from flask import Flask
from sqlalchemy_utils import database_exists, drop_database

from omdb.config import config
from omdb.db.base import BaseModel, MetaData, StringColumn, TextColumn, UtcDateTimeColumn, _UtcDateTime, setup_db
from tests.conftest import BaseTest


class TestSetupDB(BaseTest):
    @pytest.fixture
    def app(self, monkeypatch):
        monkeypatch.setattr(config, 'SQLALCHEMY_DATABASE_URI', f'sqlite:///{__name__}.db')
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
        yield app
        drop_database(config.SQLALCHEMY_DATABASE_URI)

    def test_setup_db_creates_database(self, app):
        with app.app_context():
            assert not database_exists(config.SQLALCHEMY_DATABASE_URI)
            setup_db(app)
            assert database_exists(config.SQLALCHEMY_DATABASE_URI)


class TestBaseColumns(BaseTest):
    def test_utc_datetime_column(self):
        now_utc = datetime.datetime.now(pytz.utc)
        column = UtcDateTimeColumn(default=now_utc)
        value = column.default.arg
        assert isinstance(value, datetime.datetime)
        assert value.tzinfo == pytz.utc
        assert column.index is False
        assert column.nullable is False

    def test_string_column(self):
        column = StringColumn()
        assert column.type.length == 100

        custom_max_length = 50
        column = StringColumn(max_length=custom_max_length)
        assert column.type.length == custom_max_length

    def test_text_column(self):
        column = TextColumn()
        assert column.type.length == 30000

        custom_max_length = 10000
        column = TextColumn(max_length=custom_max_length)
        assert column.type.length == custom_max_length

    def test_base_model(self):
        assert BaseModel.metadata is not None
        assert isinstance(BaseModel.metadata, MetaData)


class TestUtcDateTime(BaseTest):
    def test_process_bind_param(self):
        tz_datetime = _UtcDateTime()
        input_datetime = datetime.datetime.now(pytz.utc)
        result = tz_datetime.process_bind_param(input_datetime, None)
        assert result == input_datetime

    def test_process_bind_param_with_none_value(self):
        tz_datetime = _UtcDateTime()
        result = tz_datetime.process_bind_param(None, None)
        assert result is None

    def test_process_bind_param_raises_error_for_naive_datetime(self):
        tz_datetime = _UtcDateTime()
        naive_datetime = datetime.datetime(2023, 12, 1)

        with pytest.raises(ValueError):
            tz_datetime.process_bind_param(naive_datetime, None)

        with pytest.raises(TypeError):
            tz_datetime.process_bind_param('invalid', None)

    def test_process_result_value(self):
        tz_datetime = _UtcDateTime()
        input_datetime = datetime.datetime(2023, 12, 1, tzinfo=None)
        result = tz_datetime.process_result_value(input_datetime, None)
        assert result == input_datetime.replace(tzinfo=datetime.timezone.utc)

    def test_process_result_value_with_none_value(self):
        tz_datetime = _UtcDateTime()
        result = tz_datetime.process_result_value(None, None)
        assert result is None
