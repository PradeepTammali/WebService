# -*- coding: utf-8 -*-
import datetime

from sqlalchemy import Column, Integer, String

from omdb.db.model import Model
from tests.conftest import BaseTest


class BasicTestModel(Model):
    __tablename__ = 'test_model'

    id = Column(Integer, primary_key=True)
    value = Column(String)
    value2 = Column(String)
    value3 = Column(String)

    def __init__(self, value, value2, value3):
        super().__init__()

        self.value = value
        self.value2 = value2
        self.value3 = value3


class TestDatabase(BaseTest):
    def test_model(self) -> None:
        test = BasicTestModel('foo1', 'bar1', 'baz')
        test.save()
        assert test.class_name == BasicTestModel.__name__
        assert test.id
        assert isinstance(test.created, datetime.datetime)
        assert isinstance(test.updated, datetime.datetime)
        assert test.value == 'foo1'
        assert test.value2 == 'bar1'
        assert test.value3 == 'baz'
        test.delete()
