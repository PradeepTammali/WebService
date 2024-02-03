# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS

from omdb import log
from omdb.config import config
from omdb.db.base import setup_db
from omdb.request_hooks import app as request_hooks_blueprint
from omdb.routes.movie import movies as movie_blueprints
from omdb.utils.build_db import populate_database


def create_app(name: str) -> Flask:
    app = Flask(name)
    CORS(app)

    # App setup
    app.config.from_object(config)
    log.setup()
    setup_db(app=app)
    populate_database(app=app)

    # Register common blueprints
    app.register_blueprint(request_hooks_blueprint)

    # Register blueprints
    app.register_blueprint(movie_blueprints)

    return app
