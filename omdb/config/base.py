# -*- coding: utf-8 -*-
from enum import Enum

from omdb.config.environment import get_environment, is_running_in_docker


class DateFormat(Enum):
    YYYY_MM_DD = '%Y-%m-%d'  # default
    MM_DD_YYYY = '%m-%d-%Y'
    DD_MM_YYYY = '%d-%m-%Y'


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


class EnvironmentConfig(BaseConfig):
    API_PREFIX = '/api'
    TESTING = False
    DEBUG = False

    # Default logging levels
    LOGGING_LOGGER_LEVELS: dict[str, str] = {
        'console': 'INFO',
        'docker': 'INFO',
        'syslog': 'INFO',
    }

    # Standard datetime format
    DATE_TIME_FORMAT = f'{DateFormat.YYYY_MM_DD.value} {TimeFormat.HH_MM_SS.value}'
    DATE_TIME_FORMAT_TZ = f'{DateFormat.YYYY_MM_DD.value}T{TimeFormat.HH_MM_SS_TZ.value}'
