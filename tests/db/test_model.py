# -*- coding: utf-8 -*-
import datetime

from tests.conftest import BaseTest, BaseTestModel


class TestDatabase(BaseTest):
    def test_model(self):
        test = BaseTestModel('foo1', 'bar1', 'baz')
        test.save()
        assert test.class_name == BaseTestModel.__name__
        assert test.id
        assert isinstance(test.created, datetime.datetime)
        assert isinstance(test.updated, datetime.datetime)
        assert test.value == 'foo1'
        assert test.value2 == 'bar1'
        assert test.value3 == 'baz'
        test.delete()
