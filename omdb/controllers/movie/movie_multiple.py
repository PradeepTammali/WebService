# -*- coding: utf-8 -*-
from omdb.models.movie import Movie


class MovieMultipleController:
    def __init__(self, limit: int, offset: int):
        self.limit = limit
        self.offset = offset

    def run(self):
        movies = Movie.lookup(sort_by='title', limit=self.limit, offset=self.offset)
        return movies
