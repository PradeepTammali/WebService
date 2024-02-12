# -*- coding: utf-8 -*-
from flask import Response

from omdb.controllers.movie.movie_one import MovieOneController
from omdb.exceptions.base import OmdbModelNotFoundException
from omdb.schema.movie import MovieSchema
from omdb.utils.http import error, success


def movie_one(title: str) -> Response:
    try:
        controller = MovieOneController(title=title)
        movie = controller.run()
    except OmdbModelNotFoundException:
        return error(400, f'Movie with title "{title}" not found')

    return success(response_data=movie, schema=MovieSchema())
