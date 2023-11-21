# -*- coding: utf-8 -*-
from omdb.config.base import EnvironmentConfig


class DevelopmentConfig(EnvironmentConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = ''
