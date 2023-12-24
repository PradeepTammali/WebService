# -*- coding: utf-8 -*-
from omdb.config.base import DateFormat
from omdb.models.movie import OmdbResultType
from omdb.schema import fields
from omdb.schema.base import ModelSchema


class RatingSchema(ModelSchema):
    source = fields.Str()
    value = fields.Str()


class MovieSchema(ModelSchema):
    title = fields.Str()
    year = fields.Str()
    rated = fields.Str()
    released = fields.UtcDateTime(format=DateFormat.DD_BB_YYYY.value)
    runtime = fields.Str()
    genre = fields.Str()
    director = fields.Str()
    writer = fields.Str()
    actors = fields.Str()
    plot = fields.Str()
    language = fields.Str()
    country = fields.Str()
    awards = fields.Str()
    poster = fields.Url()
    ratings = fields.Nested(RatingSchema, many=True)
    metascore = fields.Int()
    imdb_rating = fields.Float()
    imdb_votes = fields.Str()
    imdb_id = fields.Str(required=True, allow_none=False)
    type = fields.EnumField(OmdbResultType, validate=fields.Equal(OmdbResultType.MOVIE), by_value=True)
    dvd = fields.Str()
    box_office = fields.Str()
    production = fields.Str()
    website = fields.Str()
    response = fields.Bool()
