# -*- coding: utf-8 -*-
from flask import Response

from omdb.controllers.movie_delete import MovieDeleteController
from omdb.exceptions.base import OmdbModelNotFoundException
from omdb.utils.http import error, success


def movie_delete(movie_id: int) -> Response:
    try:
        controller = MovieDeleteController(movie_id=movie_id)
        controller.run()
    except OmdbModelNotFoundException:
        return error(400, f'Movie with id "{movie_id}" not found')

    return success()