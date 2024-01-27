# -*- coding: utf-8 -*-
from flask import Blueprint
from sqlalchemy import Column, Integer
from werkzeug.exceptions import BadRequest, InternalServerError

from omdb.db.base import StringColumn
from omdb.db.model import Model
from omdb.db.query import BaseQueryList
from omdb.schema import fields
from omdb.schema.base import ModelSchema
from omdb.utils.http import error, success, validate_schema


class BaseTestSchema(ModelSchema):
    value = fields.Str(required=True)
    value2 = fields.Str(required=True)
    value3 = fields.Str(required=True)


class BaseTestModelQueryList(BaseQueryList['BaseTestModel']):
    pass


class BaseTestModel(Model):
    __tablename__ = 'test_model'
    querylist = BaseTestModelQueryList

    id = Column(Integer, primary_key=True)
    value = StringColumn()
    value2 = StringColumn()
    value3 = StringColumn()

    def __init__(self, value, value2, value3):
        super().__init__()

        self.value = value
        self.value2 = value2
        self.value3 = value3


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
