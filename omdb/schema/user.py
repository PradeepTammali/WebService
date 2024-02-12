# -*- coding: utf-8 -*-
from omdb.schema import fields
from omdb.schema.base import ModelSchema


class UserSchema(ModelSchema):
    email = fields.Str()
    is_admin = fields.Bool()
