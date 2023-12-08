# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, TypeVar

from sqlalchemy import asc, desc
from sqlalchemy.exc import MultipleResultsFound

from omdb.db.base import db
from omdb.exceptions.base import OmdbQueryException, OmdbQueryMultipleResultsException

if TYPE_CHECKING:
    from sqlalchemy.orm import Query

    from omdb.db.model import Model

ModelT = TypeVar('ModelT', bound='Model')


class BaseQueryList(list[ModelT]):
    def save(self) -> BaseQueryList[ModelT]:
        querylist: BaseQueryList = self.__class__()
        for model in self:
            querylist.append(model.save())

        return querylist

    def get_ids(self) -> list[int]:
        return self.get_values()

    def get_values(self, key: str = 'id') -> list[Any]:
        return [getattr(x, key) for x in self]

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}'


class BaseQuery:
    querylist: type[BaseQueryList]

    @classmethod
    def _get_order_dir(cls, field: str) -> tuple[str, Callable]:
        if field[0] == '-':
            return field[1:], desc
        return field, asc

    @classmethod
    def lookup(
        cls: type[BaseQuery | Model],
        sort_by: str = None,
        **kwargs: dict,
    ) -> BaseQueryList[ModelT]:
        query: Query = db.select(cls).filter_by(**kwargs)

        if sort_by:
            key, func = cls._get_order_dir(sort_by)
            query = query.order_by(func(key))

        result = db.session.execute(query).scalars()
        return cls.querylist(result)

    @classmethod
    def one(cls: type[BaseQuery | Model], **kwargs: dict) -> Model:
        if not kwargs:
            raise OmdbQueryException('DB: Do not forget attributes!')

        result = db.one_or_404(db.select(cls).filter_by(**kwargs))
        return result

    @classmethod
    def one_or_none(cls: type[BaseQuery | Model], **kwargs: dict) -> Model | None:
        if not kwargs:
            raise OmdbQueryException('DB: Do not forget attributes!')

        try:
            result = db.session.execute(db.select(cls).filter_by(**kwargs)).scalar_one_or_none()
        except MultipleResultsFound as e:
            raise OmdbQueryMultipleResultsException from e

        return result
