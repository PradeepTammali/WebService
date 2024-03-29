# -*- coding: utf-8 -*-
import datetime
from dataclasses import dataclass

import pytz
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, MetaData, String, Text
from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.types import TypeDecorator
from sqlalchemy_utils import create_database, database_exists

from omdb.config import config

convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
}
metadata = MetaData(naming_convention=convention)


class StringColumn(Column):
    inherit_cache = True

    def __init__(self, max_length: int = 100, collation: str | None = None, **columnkwargs):
        column = String(length=max_length, collation=collation)
        super().__init__(column, **columnkwargs)


class TextColumn(Column):  # pylint: disable=abstract-method, too-many-ancestors
    inherit_cache = True

    def __init__(self, max_length: int = 30000, collation: str | None = None, **columnkwargs):
        column = Text(length=max_length, collation=collation)
        super().__init__(column, **columnkwargs)


class UtcDateTimeColumn(Column):  # pylint: disable=too-many-ancestors, abstract-method
    inherit_cache = True

    def __init__(
        self,
        default: datetime.datetime = None,
        index: bool = False,
        nullable: bool = False,
        **columnkwargs: dict,
    ):
        column = _UtcDateTime()
        super().__init__(column, default=default, index=index, nullable=nullable, **columnkwargs)


class _UtcDateTime(TypeDecorator):  # pylint: disable=too-many-ancestors, abstract-method
    """Almost equivalent to :class:`~sqlalchemy.types.DateTime` with
    ``timezone=True`` option, but it differs from that by:
    - Never silently take naive :class:`~datetime.datetime`, instead it
      always raise :exc:`ValueError` unless time zone aware value.
    - :class:`~datetime.datetime` value's :attr:`~datetime.datetime.tzinfo`
      is only allowed when specified as pytz.utc
    - Unlike SQLAlchemy's built-in :class:`~sqlalchemy.types.DateTime`,
      it never return naive :class:`~datetime.datetime`, but time zone
      aware value, even with SQLite or MySQL.
    """

    impl = DateTime(timezone=True)
    cache_ok = True

    def process_bind_param(self, value: datetime.datetime | None, dialect: Dialect) -> datetime.datetime | None:
        del dialect

        if value is not None:
            if not isinstance(value, datetime.datetime):
                raise TypeError(f'expected datetime.datetime, not {value}')

            if value.tzinfo != pytz.utc:
                raise ValueError('non-utc (pytz.utc) timezones is disallowed')

        return value

    def process_result_value(self, value: datetime.datetime | None, dialect: Dialect) -> datetime.datetime | None:
        del dialect

        if value is not None and value.tzinfo is None:
            value = value.replace(tzinfo=pytz.utc)

        return value


@dataclass
class BaseModel(DeclarativeBase):
    metadata = metadata


db: SQLAlchemy = SQLAlchemy(model_class=BaseModel)


def setup_db(app: Flask):
    if not database_exists(config.SQLALCHEMY_DATABASE_URI):
        create_database(config.SQLALCHEMY_DATABASE_URI)

    db.init_app(app=app)
    with app.app_context():
        db.create_all()
