from flask import Flask
from flask_cors import CORS

from omdb import log


def create_app(name: str) -> Flask:
    app = Flask(name)
    CORS(app)
    log.setup()

    return app
