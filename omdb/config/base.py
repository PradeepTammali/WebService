# -*- coding: utf-8 -*-
import os
from dataclasses import dataclass
from enum import Enum

from omdb.config.environment import get_environment, is_running_in_docker


class DateFormat(Enum):
    YYYY_MM_DD = '%Y-%m-%d'  # default
    MM_DD_YYYY = '%m-%d-%Y'
    DD_MM_YYYY = '%d-%m-%Y'
    DD_BB_YYYY = '%d %b %Y'


class TimeFormat(Enum):
    HH_MM_SS = '%H:%M:%S'  # default
    HH_MM_SS_TZ = '%H:%M:%S%z'


class BaseConfig:
    ENVIRONMENT = get_environment()
    IS_DOCKER = is_running_in_docker()

    def is_production(self) -> bool:
        return self.ENVIRONMENT == 'production'

    def is_development(self) -> bool:
        return self.ENVIRONMENT == 'development'

    def is_test(self) -> bool:
        return self.ENVIRONMENT == 'test'

    def is_unittest(self) -> bool:
        return self.ENVIRONMENT == 'unittest'


@dataclass
class AppConfig:
    DEBUG = False
    TESTING = False


class EnvironmentConfig(BaseConfig, AppConfig):
    API_PREFIX = '/api'

    # Default logging levels
    LOGGING_LOGGER_LEVELS: dict[str, str] = {
        'console': 'INFO',
        'docker': 'INFO',
        'syslog': 'INFO',
    }

    # Standard datetime format
    DATE_TIME_FORMAT = f'{DateFormat.YYYY_MM_DD.value} {TimeFormat.HH_MM_SS.value}'
    DATE_TIME_FORMAT_TZ = f'{DateFormat.YYYY_MM_DD.value}T{TimeFormat.HH_MM_SS_TZ.value}'

    # OMDB API config
    OMDB_API_KEY = os.getenv('OMDB_API_KEY', '1b4aea85')
    OMDB_DATA_TYPE = os.getenv('OMDB_DATA_TYPE', 'movie')
    OMDB_SEARCH_KEY = os.getenv('OMDB_SEARCH_KEY', 'avengers')

    # Database default name
    MYSQL_DEFAULT_DB_NAME = 'omdb'
    SQLALCHEMY_ECHO = False

    SECRET_KEY = os.getenv('SECRET_KEY', 'AvC5e_5bEU868BK2XPRb7RTBlGO9OuVJfwT3VvsdCLU')
    DEFAULT_USER_EMAIL = os.getenv('DEFAULT_USER', 'admin@omdb.com')
    DEFAULT_USER_PASSWORD = os.getenv('DEFAULT_USER_PASSWORD', 'password1234')

    def __init__(self):
        # Database configuration
        _mysql_db_user = os.getenv('SERVICE_DATABASE_USER')
        _mysql_db_password = os.getenv('SERVICE_DATABASE_PASSWORD')
        _mysql_db_host = os.getenv('SERVICE_DATABASE_HOST')
        _mysql_db_port = os.getenv('SERVICE_DATABASE_PORT')
        _mysql_db_name = os.getenv('SERVICE_DATABASE_NAME', self.MYSQL_DEFAULT_DB_NAME)

        # SQLite as fallback database
        self.SQLALCHEMY_DATABASE_URI = f'sqlite:///{_mysql_db_name}.db'  # pylint: disable=invalid-name

        # MySQL
        if all([_mysql_db_user, _mysql_db_password, _mysql_db_host, _mysql_db_port, _mysql_db_name]):
            self.SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{_mysql_db_user}:{_mysql_db_password}@{_mysql_db_host}:{_mysql_db_port}/{_mysql_db_name}'
