# -*- coding: utf-8 -*-
from omdb.models.movie import Movie


class MovieDeleteController:
    def __init__(self, movie_id: int):
        self.movie_id = movie_id

        self.movie: Movie
        self._init_movie()

    def _init_movie(self):
        self.movie = Movie.one(id=self.movie_id)

    def run(self):
        self.movie.delete()
