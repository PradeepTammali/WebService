# -*- coding: utf-8 -*-
from omdb.config.base import EnvironmentConfig


class ProductionConfig(EnvironmentConfig):
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = ''
