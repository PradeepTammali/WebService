# -*- coding: utf-8 -*-
from datetime import datetime

import pytz
from marshmallow import pre_load
from marshmallow.fields import Bool, DateTime, Field, Float, Int, Nested, Str, Url
from marshmallow.validate import Equal, Range
from marshmallow_enum import EnumField


class UtcDateTime(DateTime):
    """A validated DateTime which deserialize in UTC datetime"""

    def _deserialize(self, value, attr, data, **kwargs) -> datetime:
        value = super()._deserialize(value, attr, data, **kwargs)

        if value.tzinfo is None:
            value = value.replace(tzinfo=pytz.utc)

        return value.astimezone(tz=pytz.utc)


class ID(Int):
    """A validated Int field that accepts unsigned integers excluding 0."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.validators.insert(0, Range(min=1, max=4294967295))  # max value of int(11) = 2 ** 32 - 1


__all__ = [
    'pre_load',
    'Bool',
    'DateTime',
    'Field',
    'Float',
    'Int',
    'Nested',
    'Str',
    'Url',
    'Equal',
    'Range',
    'EnumField',
    'UtcDateTime',
    'ID',
]
