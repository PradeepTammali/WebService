# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer

from omdb.db.base import StringColumn
from omdb.db.model import Model
from omdb.db.query import BaseQueryList
from omdb.models.user import User
from omdb.schema import fields
from omdb.schema.base import ModelSchema


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


class BaseUserModel(User):
    def __init__(  # pylint: disable=too-many-arguments
        self,
        email: str,
        password: str,
        admin: bool = False,
        remember: bool = False,
        force: bool = False,
        fresh: bool = False,
    ):
        self.remember = remember
        self.force = force
        self.fresh = fresh
        super().__init__(email=email, password=password, is_admin=admin)
