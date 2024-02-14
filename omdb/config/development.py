# -*- coding: utf-8 -*-
import os

from omdb.config.base import EnvironmentConfig
from omdb.utils.hashers import random_hash16


class DevelopmentConfig(EnvironmentConfig):
    DEBUG = bool(int(os.getenv('FLASK_DEBUG', '1')))
    TESTING = False

    _log_level = 'DEBUG' if DEBUG else 'INFO'
    LOGGING_LOGGER_LEVELS: dict[str, str] = {
        'console': _log_level,
        'docker': _log_level,
        'syslog': _log_level,
    }


class UnitTestConfig(DevelopmentConfig):
    DEBUG = True
    TESTING = True

    # Pytest database
    MYSQL_DEFAULT_DB_NAME = 'test'

    # Flask-Login settings
    # session protection shold be disabled for testing
    SESSION_PROTECTION = None
    SESSION_PERMANENT = False
    SECRET_KEY = random_hash16()
    REMEMBER_COOKIE_REFRESH_EACH_REQUEST = False

    # CSRF protection should be disabled for testing
    WTF_CSRF_ENABLED = False
