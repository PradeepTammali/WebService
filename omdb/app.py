from flask import Flask
from flask_cors import CORS

from omdb import config


def create_app(name: str) -> Flask:
    config.setup()
    app = Flask(name)
    CORS(app)

    return app
