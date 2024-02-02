# -*- coding: utf-8 -*-
from flask import Response

from omdb.controllers.movie_create import MovieCreateController
from omdb.exceptions.base import OmdbInvalidDataException
from omdb.schema.movie import MovieSchema
from omdb.utils.http import error, success, validate_schema


@validate_schema(schema=MovieSchema(exclude=('type', 'response')))
def movie_create(request_data: dict) -> Response:
    try:
        controller = MovieCreateController(**request_data)
        movie = controller.run()
    except OmdbInvalidDataException as e:
        return error(400, str(e))

    return success(response_data=movie, schema=MovieSchema())
