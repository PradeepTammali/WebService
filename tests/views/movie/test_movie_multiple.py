# -*- coding: utf-8 -*-
import datetime

import pytz

from omdb.config.base import DateFormat
from omdb.models.movie import Movie, OmdbResultType
from tests.conftest import BaseTest


class TestMovieMultipleView(BaseTest):
    ENDPOINT = '/api/movies/'

    def _prepare_movies(self):
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
        for i in range(10):
            data = test_data.copy()
            data['title'] = f'{i}{data["title"]}'
            data['imdb_id'] = f'{data["imdb_id"]}{i}'
            Movie(**data).save()

    def test_get_movie_multiple(self):
        self._prepare_movies()
        response = self.client.get(self.ENDPOINT)
        assert response.status_code == 200
        data = response.json
        assert data['count'] == 10

    def test_get_movie_multiple_paginate(self):
        self._prepare_movies()
        response = self.client.get(self.ENDPOINT + '?limit=5&offset=0')
        assert response.status_code == 200
        data = response.json
        assert data['count'] == 5
        for movie in data['collection']:
            assert movie['id'] <= 5

        response = self.client.get(self.ENDPOINT + '?limit=5&offset=5')
        assert response.status_code == 200
        data = response.json
        assert data['count'] == 5
        for movie in data['collection']:
            assert movie['id'] > 5
