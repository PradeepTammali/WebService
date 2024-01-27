# -*- coding: utf-8 -*-
from omdb.exceptions.base import OmdbModelNotFoundException
from omdb.models.movie import Movie


class MovieOneController:
    def __init__(self, title: str):
        self.title = title

    def run(self):
        movie = Movie.one_or_none(title=self.title)
        if not movie:
            raise OmdbModelNotFoundException

        return movie
