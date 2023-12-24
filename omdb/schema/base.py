# -*- coding: utf-8 -*-
from marshmallow import EXCLUDE, Schema

from omdb.config import config
from omdb.schema.fields import ID, UtcDateTime


class BaseSchema(Schema):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.unknown = kwargs.get('unknown', EXCLUDE)


class ModelSchema(BaseSchema):
    id = ID(dump_only=True)
    updated = UtcDateTime(dump_only=True, format=config.DATE_TIME_FORMAT_TZ)
    created = UtcDateTime(dump_only=True, format=config.DATE_TIME_FORMAT_TZ)
