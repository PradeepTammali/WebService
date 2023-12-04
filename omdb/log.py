# -*- coding: utf-8 -*-
import logging
import logging.config

from omdb.config import config

# Logging setup
root_logger_handler_mapper = {
    'production': ['console', 'syslog'],
    'development': ['console'],
    'test': ['console', 'syslog'],
    'unittest': ['console', 'syslog'],
}
root_logger_handlers = root_logger_handler_mapper.get(config.ENVIRONMENT, [])

DOCKER_OR_CONSOLE = 'docker' if config.IS_DOCKER else 'console'
DEFAULT_LOGGING_CONF = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            'datefmt': config.DATE_TIME_FORMAT,
        },
        'docker': {
            'format': '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "message": "%(message)s"}',
            'datefmt': config.DATE_TIME_FORMAT_TZ,
        },
        'syslog': {
            'format': 'flask: %(asctime)s - %(name)s - %(levelname)s - %(processName)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': config.LOGGING_LOGGER_LEVELS[DOCKER_OR_CONSOLE],
            'formatter': DOCKER_OR_CONSOLE,
        },
        'syslog': {
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'syslog',
            'level': config.LOGGING_LOGGER_LEVELS['syslog'],
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': config.LOGGING_LOGGER_LEVELS[DOCKER_OR_CONSOLE],
        },
        'syslog': {
            'handlers': ['syslog'],
            'level': config.LOGGING_LOGGER_LEVELS['syslog'],
        },
    },
}


def setup():
    logging.config.dictConfig(config=DEFAULT_LOGGING_CONF)


log = logging.getLogger('omdb.app')
