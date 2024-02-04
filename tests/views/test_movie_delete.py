# -*- coding: utf-8 -*-
import datetime

import pytz

from omdb.config.base import DateFormat
from omdb.models.movie import Movie, OmdbResultType
from tests.conftest import BaseTest


class TestMovieDeleteView(BaseTest):
    ENDPOINT = '/api/movies/%s'

    def test_movie_delete_400(self):
        response = self.client.json_delete(self.ENDPOINT % 1)
        assert response.status_code == 400

    def test_movie_delete(self):
        test_data = {
            'title': 'Test Movie',
            'year': '2022',
            'rated': 'PG',
            'released': datetime.datetime.strptime('01 May 2018', DateFormat.DD_BB_YYYY.value).replace(tzinfo=pytz.utc),
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
            'type_': OmdbResultType.MOVIE,
            'dvd': '2022-05-01',
            'box_office': '$10 million',
            'production': 'Test Production',
            'website': 'http://example.com',
            'response': True,
        }
        movie = Movie(**test_data).save()
        response = self.client.json_delete(self.ENDPOINT % movie.id)
        assert response.status_code == 200
