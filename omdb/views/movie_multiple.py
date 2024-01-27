# -*- coding: utf-8 -*-
from omdb.controllers.movie_multiple import MovieMultipleController
from omdb.schema.movie import MovieInputSchema, MovieSchema
from omdb.utils.http import success, validate_schema


@validate_schema(schema=MovieInputSchema())
def movie_multiple(request_data: dict):
    limit: int = request_data['limit']
    offset: int = request_data['offset']

    controller = MovieMultipleController(limit=limit, offset=offset)
    movies = controller.run()

    return success(response_data=movies, schema=MovieSchema(many=True), collection=True)
