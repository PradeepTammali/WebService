# -*- coding: utf-8 -*-
import time
from datetime import datetime

import pytz
from flask import Blueprint, Response, g, request
from flask_login import current_user
from werkzeug.exceptions import InternalServerError, NotFound

from omdb.config import config
from omdb.db.base import db
from omdb.log import log
from omdb.login_manager import login_manager
from omdb.models.user import User
from omdb.utils.hashers import generate_request_id
from omdb.utils.http import success

app = Blueprint('request_hooks', __name__, url_prefix='/')

# TODO: add request logs to the database
# TODO: add test cases properly


@login_manager.user_loader
def load_user(user_email: str) -> User | None:
    return User.one_or_none(email=user_email)


@app.before_app_request
def before_request():
    if request.path == '/api/health_check':
        return success()

    # Fix automatic routing without when a slash is missing
    if request.routing_exception:
        raise NotFound(f'Endpoint not found, did you mean "{request.path}/"? (note the trailing slash)')

    # Used by transaction log and response headers (place as close to start as possible)
    g.request_time = time.time()

    # A unique ID so that we can track each request in the logs
    g.request_id = generate_request_id()

    if request.path.startswith('/api/'):
        log.debug('request (before) - request on url %s with method %s', request.full_path, request.method)

    if current_user.is_anonymous:
        log.debug('Anonymous user accessing url %s with method %s', request.full_path, request.method)

    if current_user.is_authenticated:
        log.info(
            '[access_log] endpoint=%(endpoint)s user_id=%(user_id)s is_admin=%(is_admin)s ',
            {
                'user_id': current_user.id,
                'is_admin': current_user.is_admin,
                'endpoint': request.endpoint,
            },
        )

    return None


@app.after_app_request
def after_request(response: Response):
    # Fix automatic routing without when a slash is missing
    if request.routing_exception:
        return response

    if request.path.startswith('/api/'):
        log.debug(
            'request (after) - request on url %s with method %s and status %s',
            request.full_path,
            request.method,
            response.status,
        )

    # Debug headers (only)
    response.headers['X-OMDB-Server-Time'] = datetime.now(tz=pytz.utc)
    response.headers['X-OMDB-API-Version'] = '1.0'
    response.headers['X-OMDB-Environment'] = config.ENVIRONMENT
    response.headers['X-OMDB-Request-ID'] = g.request_id

    # Security headers
    response.headers['Strict-Transport-Security'] = 'max-age=31536000'
    response.headers['Referrer-Policy'] = 'strict-origin'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['X-Content-Type-Options'] = 'nosniff'

    if response.status_code not in [200, 201, 202, 204, 301, 302]:
        db.session.rollback()
        return response

    try:
        db.session.commit()
    except Exception as e:
        response.headers['X-Flow-Request-Time'] = f'{((time.time() - g.request_time) * 1000)}.0f'
        log.error('request (after) - db commit failed: %s', str(e))
        raise InternalServerError(f'request (after) - db commit failed: {str(e)}') from e

    return response


@app.teardown_app_request
def teardown(exception=None):
    if exception:
        log.error(exception)

    db.session.remove()
