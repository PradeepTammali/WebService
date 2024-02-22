# -*- coding: utf-8 -*-
from datetime import datetime

import pytz
from marshmallow import pre_load
from marshmallow.fields import Bool, DateTime, Enum, Field, Float, Int, Nested, Str, Url
from marshmallow.validate import Equal, Range


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


class Limit(Int):
    """Pagination limit field with default load_default=10 and min=0 and max=100.
    Max can only be overriden by Range validator, min cannot be overriden.
    """

    def __init__(self, *args, maximum=100, load_default=10, **kwargs):
        # min and max are our custom args
        # load_default and load_only are marshmallow args
        kwargs['load_default'] = load_default
        kwargs['load_only'] = True
        super().__init__(*args, **kwargs)

        self.validators.insert(0, Range(min=1, max=maximum))


__all__ = [
    'pre_load',
    'Bool',
    'DateTime',
    'Enum',
    'Field',
    'Float',
    'Int',
    'Nested',
    'Str',
    'Url',
    'Equal',
    'Range',
    'UtcDateTime',
    'ID',
    'Limit',
]
