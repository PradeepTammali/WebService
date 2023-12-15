# -*- coding: utf-8 -*-
from flask import Flask

from omdb.config import config
from omdb.db.base import db


def populate_database(app: Flask):
    if config.is_unittest():
        return

    with app.app_context():
        db.create_all()
