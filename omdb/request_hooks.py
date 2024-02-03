# -*- coding: utf-8 -*-
from flask import Blueprint, Response

from omdb.db.base import db
from omdb.log import log

app = Blueprint('request_hooks', __name__, url_prefix='/')

# TODO: add request logs to the database
# TODO: calcuate request time and set response headers
# TODO: exception handling if commit fails and logging
# TODO: add test cases properly


@app.before_app_request
def before_request():
    pass


@app.after_app_request
def after_request(response: Response):
    if response.status_code not in [200, 201, 202, 204, 301, 302]:
        db.session.rollback()
        return response

    db.session.commit()
    return response


@app.teardown_app_request
def teardown(exception=None):
    if exception:
        log.error(exception)

    db.session.remove()
