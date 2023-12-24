# -*- coding: utf-8 -*-
from marshmallow import EXCLUDE

from omdb.schema.base import BaseSchema
from tests.conftest import BaseTest


class TestBaseSchema(BaseTest):
    def test_init(self):
        base_schema = BaseSchema()
        assert base_schema.unknown == EXCLUDE
