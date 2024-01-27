# -*- coding: utf-8 -*-
import traceback
from functools import wraps
from typing import Any, Union

from flask import Response, jsonify, request
from marshmallow import Schema, ValidationError

from omdb.db.model import Model
from omdb.db.query import BaseQueryList
from omdb.log import log


def validate_schema(schema: Schema = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not schema:
                return func(*args, **kwargs)

            if request.method == 'GET':
                data = request.args.to_dict()
            else:
                if not (
                    request.content_type
                    and request.content_type.lower() in ['application/json', 'application/json; charset=utf-8']
                ):
                    return error(400, 'Invalid content type, must be application/json')
                data = request.get_json(silent=True)

            if data is None:
                return error(400, 'Invalid JSON format, failed to parse the request body')

            try:
                request_data = schema.load(data)
            except ValidationError as e:
                return error(
                    400,
                    'Request data format invalid. See field errors for details.',
                    extra_keys={'field_errors': e.messages},
                )

            kwargs.update({'request_data': request_data})
            return func(*args, **kwargs)

        return wrapper

    return decorator


def error(code: int, text: str = None, extra_keys: dict[str, Any] = None) -> Response:
    if not extra_keys:
        extra_keys = {}

    if text is None:
        text = 'Something went wrong.'

    if extra_keys.get('exception'):
        exc_traceback = extra_keys['exception'].__traceback__

        stacktrace = traceback.extract_tb(exc_traceback)
        extra_keys['caused_by'] = tuple(stacktrace[-1]) if stacktrace else None
    else:
        stacktrace = traceback.extract_stack()
        extra_keys['caused_by'] = tuple(stacktrace[-2]) if stacktrace else None

    log.debug('Logged error with code: "%s", text: "%s", extra keys: %s', code, text, extra_keys)

    # Suppress actual errors when sending things to the client
    if code == 500:
        text = 'Internal server error'

    if extra_keys.get('exception'):
        del extra_keys['exception']

    if extra_keys.get('caused_by'):
        del extra_keys['caused_by']

    response = jsonify(dict({'error': text, 'status_code': code}, **extra_keys))
    response.status_code = int(code)
    response.mimetype = 'application/json'
    response.content_type = 'application/json; charset=UTF-8'

    return response


def success(
    response_data: Union[Model, BaseQueryList, Any] = None,
    schema: Schema = None,
    collection: bool = False,
    count: int = None,
    mimetype: str = 'application/json',
    **kwargs,
) -> Response:
    if response_data is None:
        response_data = [] if collection is True else {}

    output = schema.dump(response_data) if schema else response_data

    if isinstance(output, list):
        if count is None:
            count = len(output)

        final_output = {
            'collection': output,
            'count': count,
        }
    else:
        final_output = output

    if kwargs:
        final_output.update(kwargs)

    # Create output with correct mimetype
    response = jsonify(final_output)
    response.mimetype = mimetype
    response.content_type = f'{mimetype}; charset=UTF-8'
    return response
