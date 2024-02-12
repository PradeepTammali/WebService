# -*- coding: utf-8 -*-
from flask import Blueprint

from omdb.utils.http import error, success

request_hooks_blueprint = Blueprint('test_request_hooks', __name__, url_prefix='/test_request_hooks')


@request_hooks_blueprint.route('/', methods=['GET', 'POST'])
def endpoint_success():
    return success()


@request_hooks_blueprint.route('/error', methods=['GET', 'POST'])
def endpoint_error():
    return error(404, 'Not found')
