# -*- coding: utf-8 -*-
from pytest import MonkeyPatch

from omdb.config.base import BaseConfig, DateFormat, EnvironmentConfig, TimeFormat
from tests.conftest import BaseTest


class TestBaseConfig(BaseTest):
    def test_production_environment(self):
        config = BaseConfig()
        config.ENVIRONMENT = 'production'
        assert config.is_production()
        assert not config.is_development()
        assert not config.is_test()
        assert not config.is_unittest()

    def test_development_environment(self):
        config = BaseConfig()
        config.ENVIRONMENT = 'development'
        assert not config.is_production()
        assert config.is_development()
        assert not config.is_test()
        assert not config.is_unittest()

    def test_test_environment(self):
        config = BaseConfig()
        config.ENVIRONMENT = 'test'
        assert not config.is_production()
        assert not config.is_development()
        assert config.is_test()
        assert not config.is_unittest()

    def test_unittest_environment(self):
        config = BaseConfig()
        config.ENVIRONMENT = 'unittest'
        assert not config.is_production()
        assert not config.is_development()
        assert not config.is_test()
        assert config.is_unittest()


class TestEnvironmentConfig(BaseTest):
    def test_default_values(self):
        config = EnvironmentConfig()
        assert not config.DEBUG
        assert not config.TESTING
        assert config.API_PREFIX == '/api'
        assert config.LOGGING_LOGGER_LEVELS == {
            'console': 'INFO',
            'docker': 'INFO',
            'syslog': 'INFO',
        }
        assert config.DATE_TIME_FORMAT == f'{DateFormat.YYYY_MM_DD.value} {TimeFormat.HH_MM_SS.value}'
        assert config.DATE_TIME_FORMAT_TZ == f'{DateFormat.YYYY_MM_DD.value}T{TimeFormat.HH_MM_SS_TZ.value}'
        assert config.MYSQL_DEFAULT_DB_NAME == 'omdb'
        assert config.SQLALCHEMY_ECHO is False

    def test_init_with_environment_variables(self, monkeypatch: MonkeyPatch):
        monkeypatch.setenv('SERVICE_DATABASE_USER', 'test_user')
        monkeypatch.setenv('SERVICE_DATABASE_PASSWORD', 'test_password')
        monkeypatch.setenv('SERVICE_DATABASE_HOST', 'localhost')
        monkeypatch.setenv('SERVICE_DATABASE_PORT', '3306')
        monkeypatch.setenv('SERVICE_DATABASE_NAME', 'test_db')

        config = EnvironmentConfig()

        # Updated SQLite URI
        assert config.SQLALCHEMY_DATABASE_URI == 'mysql+pymysql://test_user:test_password@localhost:3306/test_db'
