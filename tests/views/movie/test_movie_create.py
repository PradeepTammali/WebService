# -*- coding: utf-8 -*-
import pytest

from omdb.models.movie import Movie
from tests.conftest import BaseTest


class TestMovieCreateView(BaseTest):
    ENDPOINT = '/api/movies/'

    @pytest.fixture
    def movie_data(self) -> dict:
        return {
            'title': 'Test Movie',
            'year': '2022',
            'rated': 'PG',
            'released': '05 Jun 2000',
            'runtime': '120 min',
            'genre': 'Action',
            'director': 'John Doe',
            'writer': 'Jane Doe',
            'actors': 'Actor 1, Actor 2',
            'plot': 'Test plot',
            'language': 'English',
            'country': 'USA',
            'awards': 'Test Award',
            'poster': 'http://example.com/poster.jpg',
            'metascore': 80,
            'imdb_rating': 7.5,
            'imdb_votes': '1000',
            'imdb_id': 'tt1234567',
            'dvd': '2022-05-01',
            'box_office': '$10 million',
            'production': 'Test Production',
            'website': 'http://example.com',
            'response': True,
            'ratings': [
                {
                    'source': 'Internet Movie Database',
                    'value': '8.5/10',
                },
                {
                    'source': 'Random Database',
                    'value': '7/10',
                },
            ],
        }

    def test_create_already_exist(self, movie_data: dict):
        response = self.client.json_post(self.ENDPOINT, json=movie_data)
        assert response.status_code == 200

        response = self.client.json_post(self.ENDPOINT, json=movie_data)
        assert response.status_code == 400

    def test_create(self, movie_data: dict):
        response = self.client.json_post(self.ENDPOINT, json=movie_data)
        assert response.status_code == 200
        movie = Movie.one(imdb_id=movie_data['imdb_id'])
        assert movie.title == movie_data['title']
        assert len(movie.ratings) == 2

    def test_create_no_ratings(self, movie_data: dict):
        del movie_data['ratings']
        response = self.client.json_post(self.ENDPOINT, json=movie_data)
        assert response.status_code == 200
        movie = Movie.one(imdb_id=movie_data['imdb_id'])
        assert not movie.ratings
