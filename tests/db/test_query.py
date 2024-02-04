# -*- coding: utf-8 -*-
import pytest

from omdb.db.query import BaseQueryList
from omdb.exceptions.base import OmdbModelNotFoundException, OmdbQueryException, OmdbQueryMultipleResultsException
from tests.conftest import BaseTest
from tests.shared.base import BaseTestModel


class TestBaseQueryListSave(BaseTest):
    models: list[BaseTestModel]
    query_list: BaseQueryList[BaseTestModel]

    def setup_method(self):
        self.models = [
            BaseTestModel('foo1', 'bar1', 'baz'),
            BaseTestModel('foo1', 'bar1', 'baz'),
            BaseTestModel('foo1', 'bar1', 'baz'),
        ]
        self.query_list = BaseQueryList(self.models)

    def test_save_method(self):
        saved_query_list = self.query_list.save()
        assert isinstance(saved_query_list, BaseQueryList)
        assert self.query_list == BaseQueryList(self.models)

        for saved_model, original_model in zip(saved_query_list, self.models):
            assert saved_model == original_model
            assert saved_model.id is not None

    def test_get_ids_method(self):
        self.query_list.save()
        ids = self.query_list.get_ids()
        assert isinstance(ids, list)
        assert all(isinstance(id, int) for id in ids)
        assert ids == [1, 2, 3]

    def test_get_values_method(self):
        self.query_list.save()
        values = self.query_list.get_values(key='value')
        assert isinstance(values, list)
        assert all(isinstance(value, str) for value in values)
        assert values == ['foo1', 'foo1', 'foo1']

    def test_repr_method(self) -> None:
        self.query_list.save()
        repr_string = repr(self.query_list)
        assert 'BaseQueryList' in repr_string


class TestBaseQuery(BaseTest):
    def test_lookup(self):
        test = BaseTestModel('a', 'bar1', 'baz').save()
        result = BaseTestModel.lookup(id=test.id)
        assert isinstance(result, BaseQueryList)
        assert len(result) == 1

        BaseTestModel('b', 'bar1', 'baz').save()
        result = BaseTestModel.lookup(sort_by='value')
        assert isinstance(result, BaseQueryList)
        assert result[0].value == 'a'
        assert result[1].value == 'b'

        result = BaseTestModel.lookup(sort_by='-value')
        assert isinstance(result, BaseQueryList)
        assert result[0].value == 'b'
        assert result[1].value == 'a'

    def test_lookup_paginate(self):
        for i in range(10):
            BaseTestModel(f'foo{i}', 'bar1', 'baz').save()

        result = BaseTestModel.lookup(limit=5)
        assert isinstance(result, BaseQueryList)
        assert len(result) == 5
        for i, model in enumerate(result):
            assert model.value == f'foo{i}'

        result = BaseTestModel.lookup(limit=5, offset=5)
        assert isinstance(result, BaseQueryList)
        assert len(result) == 5
        for i, model in enumerate(result):
            assert model.value == f'foo{i+5}'

    def test_count(self):
        BaseTestModel('a', 'bar1', 'baz').save()
        BaseTestModel('b', 'bar1', 'baz').save()
        assert BaseTestModel.count() == 2

    def test_one(self):
        with pytest.raises(OmdbQueryException, match='Do not forget attributes!'):
            BaseTestModel.one()

        with pytest.raises(OmdbModelNotFoundException):
            BaseTestModel.one(id=1)

        test = BaseTestModel('foo1', 'bar1', 'baz').save()
        result = BaseTestModel.one(id=test.id)
        assert isinstance(result, BaseTestModel)
        assert result.id == 1

    def test_one_or_none(self):
        with pytest.raises(OmdbQueryException, match='Do not forget attributes!'):
            BaseTestModel.one_or_none()

        result = BaseTestModel.one_or_none(id=1)
        assert result is None

        test = BaseTestModel('foo1', 'bar1', 'baz').save()
        result = BaseTestModel.one_or_none(id=test.id)
        assert isinstance(result, BaseTestModel)
        assert result.id == 1

        BaseTestModel('foo1', 'bar1', 'baz').save()
        with pytest.raises(OmdbQueryMultipleResultsException):
            BaseTestModel.one_or_none(value='foo1')
