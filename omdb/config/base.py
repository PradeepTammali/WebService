from omdb.config.environment import get_environment, is_running_in_docker


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

    # Logging
    LOGGING_LOGGER_LEVELS: dict[str, str] = {}
    LOGGING_CONSOLE_LEVEL = 'INFO'
    LOGGING_CONFIG = 'logging.config.dictConfig'
