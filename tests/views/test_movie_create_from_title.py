# -*- coding: utf-8 -*-
from omdb.models.movie import Movie
from tests.conftest import BaseTest


class TestMovieCreateFromTitleView(BaseTest):
    ENDPOINT = '/api/movies/%s'

    def test_create_already_exist(self):
        response = self.client.json_post(self.ENDPOINT % 'avengers')
        assert response.status_code == 200

        response = self.client.json_post(self.ENDPOINT % 'avengers')
        assert response.status_code == 400

    def test_create_invalid_title(self):
        response = self.client.json_post(self.ENDPOINT % 'invalid_title')
        assert response.status_code == 500

    def test_create(self):
        response = self.client.json_post(self.ENDPOINT % 'avengers')
        assert response.status_code == 200
        movie: Movie = Movie.one(title=response.json['title'])
        assert movie.imdb_id == response.json['imdb_id']
