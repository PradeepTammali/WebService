# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS

from omdb import log
from omdb.config import config


def create_app(name: str) -> Flask:
    app = Flask(name)
    CORS(app)

    # App setup
    app.config.from_object(config)
    log.setup()

    return app
