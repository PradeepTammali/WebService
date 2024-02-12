# -*- coding: utf-8 -*-
from flask import Blueprint, Response
from werkzeug.exceptions import (
    BadRequest,
    Forbidden,
    InternalServerError,
    MethodNotAllowed,
    NotFound,
    TooManyRequests,
    Unauthorized,
)

from omdb.utils.http import error

app = Blueprint('error_handlers', __name__, url_prefix='/')


@app.app_errorhandler(BadRequest)
def error_400(e: BadRequest) -> Response:
    if e.description == BadRequest.description:
        e.description = 'The data you supplied is not accepted'

    return error(code=e.code, text=e.description, extra_keys={'exception': e})


@app.app_errorhandler(Unauthorized)
def error_401(e: Unauthorized) -> Response:
    return error(code=e.code, text=e.description, extra_keys={'exception': e})


@app.app_errorhandler(Forbidden)
def error_403(e: Forbidden) -> Response:
    return error(code=e.code, text=e.description, extra_keys={'exception': e})


@app.app_errorhandler(NotFound)
def error_404(e: NotFound) -> Response:
    if e.description == NotFound.description:
        e.description = 'The page you are trying to reach does not exist'

    return error(code=e.code, text=e.description, extra_keys={'exception': e})


@app.app_errorhandler(MethodNotAllowed)
def error_405(e: MethodNotAllowed) -> Response:
    return error(code=e.code, text=e.description, extra_keys={'exception': e})


@app.app_errorhandler(TooManyRequests)
def error_429(e: TooManyRequests):
    return error(code=e.code, text=e.description, extra_keys={'exception': e})


@app.app_errorhandler(InternalServerError)
def error_500(e: Exception) -> Response:
    # For 500 errors, the exception can be any exception.
    if not isinstance(e, InternalServerError) or e.description == InternalServerError.description:
        description = 'Internal server error'
    else:
        description = e.description

    return error(code=500, text=description, extra_keys={'exception': e})
