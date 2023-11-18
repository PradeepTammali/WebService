from omdb.config.development import DevelopmentConfig
from omdb.config.environment import get_environment
from omdb.config.production import ProductionConfig

config_mapper = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
}
_environment = get_environment()
config = config_mapper[_environment]()


def setup() -> None:
    # setup the logging levels for the app here
    pass


__all__ = ['config', 'setup']
