# -*- coding: utf-8 -*-
from flask import Response

from omdb.controllers.movie.movie_create_from_title import MovieCreateFromTitleController
from omdb.exceptions.base import OmdbInvalidDataException, OmdbRequestException
from omdb.schema.movie import MovieSchema
from omdb.utils.http import error, success


def movie_create_from_title(title: str) -> Response:
    try:
        controller = MovieCreateFromTitleController(title=title)
        movie = controller.run()
    except OmdbInvalidDataException as e:
        return error(400, 'Invalid data', extra_keys={'exception': e})
    except OmdbRequestException as e:
        return error(500, 'Could not fetch data from OMDB', extra_keys={'exception': e})

    return success(response_data=movie, schema=MovieSchema())
