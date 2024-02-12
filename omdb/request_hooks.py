# -*- coding: utf-8 -*-
from flask import Blueprint, Response

from omdb.db.base import db
from omdb.log import log
from omdb.login_manager import login_manager
from omdb.models.user import User

app = Blueprint('request_hooks', __name__, url_prefix='/')

# TODO: add request logs to the database
# TODO: calcuate request time and set response headers
# TODO: exception handling if commit fails and logging
# TODO: add test cases properly


@app.before_app_request
def before_request():
    pass


@login_manager.user_loader
def load_user(user_id: int):
    return User.one_or_none(id=user_id)


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
