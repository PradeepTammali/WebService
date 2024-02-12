# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS

from omdb import log
from omdb.config import config
from omdb.db.base import setup_db
from omdb.login_manager import bcrypt, login_manager
from omdb.request_hooks import app as request_hooks_blueprint
from omdb.routes.login import login as login_blueprints
from omdb.routes.movie import movies as movie_blueprints
from omdb.utils.build_db import populate_data


def create_app(name: str) -> Flask:
    app = Flask(name)
    CORS(app)

    # App setup
    app.config.from_object(config)
    log.setup()
    login_manager.init_app(app)
    bcrypt.init_app(app)
    setup_db(app=app)
    populate_data(app=app)

    # Register common blueprints
    app.register_blueprint(request_hooks_blueprint)

    # Register blueprints
    app.register_blueprint(movie_blueprints)
    app.register_blueprint(login_blueprints)

    return app
