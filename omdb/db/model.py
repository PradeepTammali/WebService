# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import datetime

import pytz
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr

from omdb.db.base import UtcDateTimeColumn, db
from omdb.db.query import BaseQuery, BaseQueryList


class Model(db.Model, BaseQuery):
    __abstract__ = True
    querylist: type[BaseQueryList] = BaseQueryList

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    @declared_attr
    def created(self) -> datetime:
        return UtcDateTimeColumn(default=datetime.now(tz=pytz.utc), index=True, nullable=False)

    @declared_attr
    def updated(self) -> datetime:
        return UtcDateTimeColumn(default=datetime.now(tz=pytz.utc), index=True, nullable=False)

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f'{self.class_name}.{self.id}'

    def save(self: type[Model]) -> type[Model]:
        if self not in db.session:
            db.session.add(self)

        db.session.flush()
        return self

    def delete(self: type[Model]):
        db.session.delete(self)
        db.session.flush()
