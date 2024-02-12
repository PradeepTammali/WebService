# -*- coding: utf-8 -*-
from flask import Blueprint
from werkzeug.exceptions import (
    BadRequest,
    Forbidden,
    InternalServerError,
    MethodNotAllowed,
    NotFound,
    TooManyRequests,
    Unauthorized,
)

error_handler_blueprint = Blueprint('test_api_error_handlers', __name__, url_prefix='/api/error_handlers')


@error_handler_blueprint.route('/internal_error', methods=['GET', 'POST'])
def api_url_500():
    raise InternalServerError('Internal server error')


@error_handler_blueprint.route('/internal_error2', methods=['GET', 'POST'])
def api_url_description_500():
    raise InternalServerError


@error_handler_blueprint.route('/missing_path', methods=['GET', 'POST'])
def api_url_404():
    raise NotFound('Not found')


@error_handler_blueprint.route('/missing_path2', methods=['GET', 'POST'])
def api_url_description_404():
    raise NotFound


@error_handler_blueprint.route('/forbidden', methods=['GET', 'POST'])
def api_url_403():
    raise Forbidden('Forbidden')


@error_handler_blueprint.route('/invalid', methods=['GET', 'POST'])
def api_url_400():
    raise BadRequest('The data you supplied is not accepted')


@error_handler_blueprint.route('/invalid2', methods=['GET', 'POST'])
def api_url_description_400():
    raise BadRequest


@error_handler_blueprint.route('/method_not_allowed', methods=['GET', 'POST'])
def api_url_405():
    raise MethodNotAllowed('The method is not allowed for the requested URL')


@error_handler_blueprint.route('/too_many_requests', methods=['GET', 'POST'])
def api_url_429():
    raise TooManyRequests('Too many requests')


@error_handler_blueprint.route('/unauthorized', methods=['GET', 'POST'])
def api_url_401():
    raise Unauthorized('Unauthorized')
