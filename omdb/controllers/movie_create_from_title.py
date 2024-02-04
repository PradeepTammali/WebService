# -*- coding: utf-8 -*-
from marshmallow.exceptions import ValidationError

from omdb.controllers.movie_create import MovieCreateController
from omdb.exceptions.base import OmdbRequestException
from omdb.models.movie import Movie
from omdb.schema.build_db import MovieResultSchema
from omdb.utils.request import OmdbRequest


class MovieCreateFromTitleController:
    def __init__(self, title: str):
        self.title = title

        self.omdb_api = OmdbRequest()
        self.movie: Movie
        self.movie_data: dict
        self._init_data()

    def _init_data(self):
        _movie_data = self.omdb_api.get_by_title(title=self.title)
        try:
            self.movie_data = MovieResultSchema(exclude=('type', 'response')).load(_movie_data)
        except ValidationError as e:
            raise OmdbRequestException from e

    def run(self) -> Movie:
        controller = MovieCreateController(**self.movie_data)
        self.movie = controller.run()
        return self.movie
