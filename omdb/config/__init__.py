# -*- coding: utf-8 -*-
from omdb.config.base import EnvironmentConfig
from omdb.config.development import DevelopmentConfig, UnitTestConfig
from omdb.config.environment import get_environment
from omdb.config.production import ProductionConfig

# Config setup
config_mapper = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'unittest': UnitTestConfig,
}
_environment = get_environment()
config: EnvironmentConfig = config_mapper[_environment]()


__all__ = ['config']
