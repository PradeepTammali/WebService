# -*- coding: utf-8 -*-
import os

from omdb.config.base import EnvironmentConfig


class DevelopmentConfig(EnvironmentConfig):
    DEBUG = bool(int(os.getenv('FLASK_DEBUG', '1')))
    TESTING = False

    _log_level = 'DEBUG' if DEBUG else 'INFO'
    LOGGING_LOGGER_LEVELS: dict[str, str] = {
        'console': _log_level,
        'docker': _log_level,
        'syslog': _log_level,
    }

    SQLALCHEMY_DATABASE_URI = ''
