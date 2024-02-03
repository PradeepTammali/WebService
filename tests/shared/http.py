# -*- coding: utf-8 -*-
from flask import Blueprint
from werkzeug.exceptions import BadRequest, InternalServerError

from omdb.utils.http import error, success, validate_schema
from tests.shared.base import BaseTestModel, BaseTestSchema

http_blueprint = Blueprint('http_blueprint_app', __name__, url_prefix='/api/test_http')


@http_blueprint.route('/', methods=['GET'])
@validate_schema()
def get_multiple_url():
    for i in range(5):
        BaseTestModel(value=f'foo{i}', value2=f'bar{i}', value3=f'baz{i}').save()
    base_data = BaseTestModel.lookup()
    return success(response_data=base_data, schema=BaseTestSchema(many=True), collection=True)


@http_blueprint.route('/get', methods=['GET'])
@validate_schema(schema=BaseTestSchema())
def get_url(request_data: dict):
    value = request_data['value']
    value2 = request_data['value2']
    value3 = request_data['value3']

    base_data = BaseTestModel(value=value, value2=value2, value3=value3).save()
    return success(response_data=base_data, schema=BaseTestSchema())


@http_blueprint.route('/get-one/<string:value>', methods=['GET'])
def get_one_url(value: str):
    try:
        if value == 'invalid':
            raise BadRequest

        if value == 'error':
            raise InternalServerError

        BaseTestModel(value='foo', value2='bar1', value3='baz').save()
        base_data = BaseTestModel.one_or_none(value=value)
    except BadRequest as e:
        return error(400, str(e), extra_keys={'exception': e})
    except InternalServerError as e:
        return error(500, extra_keys={'exception': e})

    return success(response_data=base_data, schema=BaseTestSchema())


@http_blueprint.route('/post', methods=['POST'])
@validate_schema(schema=BaseTestSchema())
def post_url(request_data: dict):
    value = request_data['value']
    value2 = request_data['value2']
    value3 = request_data['value3']

    base_data = BaseTestModel(value=value, value2=value2, value3=value3).save()
    return success(response_data=base_data, schema=BaseTestSchema(), sample_kwargs='sample_kwargs')
