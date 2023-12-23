# -*- coding: utf-8 -*-
from typing import Any

from omdb.schema import fields
from omdb.schema.base import BaseSchema
from omdb.schema.movie import MovieSchema, RatingSchema


def titlecase(value: str) -> str:
    return ''.join(part.title() for part in value.split('_'))


class CustomResultSchema(BaseSchema):
    def __init__(self, *args, **kwargs):
        default_excluded_fields = ('id', 'created', 'updated')
        existing_excluded_fields = kwargs.get('exclude', ())
        kwargs['exclude'] = tuple(set(existing_excluded_fields + default_excluded_fields))
        super().__init__(*args, **kwargs)

    def on_bind_field(self, field_name: str, field_obj: fields.Field):
        field_obj.data_key = field_obj.data_key or titlecase(field_name)
        field_obj.allow_none = not field_obj.required
        return super().on_bind_field(field_name, field_obj)

    def _replace_na_with_none(self, data: Any) -> Any:
        if isinstance(data, list):
            return [self._replace_na_with_none(item) for item in data]

        if isinstance(data, dict):
            return {item_key: self._replace_na_with_none(data=item) for item_key, item in data.items()}

        if isinstance(data, str) and data.lower() == 'n/a':
            return None

        return data

    @fields.pre_load()
    def replace_na_with_none(self, data: Any, **kwargs: dict) -> Any:
        del kwargs
        return self._replace_na_with_none(data=data)


class RatingResultSchema(RatingSchema, CustomResultSchema):
    pass


class MovieResultSchema(MovieSchema, CustomResultSchema):
    imdb_id = fields.Str(data_key='imdbID', required=True)
    imdb_rating = fields.Float(data_key='imdbRating')
    imdb_votes = fields.Str(data_key='imdbVotes')
    dvd = fields.Str(data_key='DVD')
    ratings = fields.Nested(RatingResultSchema, many=True)


class MovieSearchResultSchema(BaseSchema):
    search = fields.Nested(MovieResultSchema, many=True, data_key='Search', required=True)
    total_results = fields.Int(data_key='totalResults', required=True)
