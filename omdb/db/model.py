# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declared_attr

from omdb.db.base import db


class Model(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True)

    @declared_attr
    def created(self) -> datetime:
        return Column(DateTime(timezone=True), default=datetime.utcnow, index=True, nullable=False)

    @declared_attr
    def updated(self) -> datetime:
        return Column(DateTime(timezone=True), default=datetime.utcnow, index=True, nullable=False)

    @property
    def class_name(self):
        return self.__class__.__name__

    def __repr__(self):
        return f'{self.class_name}.{self.id}'

    def save(self) -> None:
        db.session.add(self)
        db.session.flush()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.flush()
