# -*- coding: utf-8 -*-
import datetime
from copy import copy

import pytest
import pytz
from sqlalchemy.exc import DataError

from omdb.config.base import DateFormat
from omdb.models.movie import Movie, OmdbResultType, Rating
from tests.conftest import BaseTest

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


class TestRatingDatabase(BaseTest):
    @pytest.fixture
    def movie_data(self) -> dict:
        return test_data

    def test_rating_model_creation(self, movie_data):
        movie = Movie(**movie_data)
        movie.save()

        rating_data = {
            'movie_id': movie.id,
            'source': 'IMDb',
            'value': '8.0',
        }

        rating = Rating(**rating_data)
        rating.save()

        assert rating.movie_id == movie.id
        assert rating.source == 'IMDb'
        assert rating.value == '8.0'

    def test_rating_model_str_representation(self, movie_data):
        movie = Movie(**movie_data)
        movie.save()

        rating_data = {
            'movie_id': movie.id,
            'source': 'IMDb',
            'value': '8.0',
        }

        rating = Rating(**rating_data)
        rating.save()

        assert str(rating) == f'{Rating.__name__}.{rating.id}'

    def test_rating_model_invalid_movie_id(self):
        with pytest.raises(ValueError):
            rating_data = {
                'movie_id': 123,  # Nonexistent movie ID
                'source': 'IMDb',
                'value': '8.0',
            }

            rating = Rating(**rating_data)
            rating.save()

    def test_rating_model_invalid_source(self):
        with pytest.raises(ValueError):
            rating_data = {
                'movie_id': 1,
                'source': 123,  # Invalid source
                'value': '8.0',
            }

            rating = Rating(**rating_data)
            rating.save()

    def test_rating_model_invalid_value(self):
        with pytest.raises(ValueError):
            rating_data = {
                'movie_id': 1,
                'source': 'IMDb',
                'value': 123,  # Invalid value
            }

            rating = Rating(**rating_data)
            rating.save()


class TestMovieDatabase(BaseTest):
    @pytest.fixture
    def movie_data(self) -> dict:
        return test_data

    def test_movie_model_initialization(self, movie_data):
        movie = Movie(**movie_data)
        movie.save()

        assert movie.class_name == Movie.__name__
        assert movie.id
        assert isinstance(movie.created, datetime.datetime)
        assert isinstance(movie.updated, datetime.datetime)
        assert movie.title == 'Test Movie'
        assert movie.year == '2022'
        assert movie.rated == 'PG'
        assert isinstance(movie.released, datetime.datetime)
        assert movie.released == datetime.datetime.strptime('01 May 2018', DateFormat.DD_BB_YYYY.value).replace(
            tzinfo=pytz.utc
        )
        assert movie.runtime == '120 min'
        assert movie.genre == 'Action'
        assert movie.director == 'John Doe'
        assert movie.writer == 'Jane Doe'
        assert movie.actors == 'Actor 1, Actor 2'
        assert movie.plot == 'Test plot'
        assert movie.language == 'English'
        assert movie.country == 'USA'
        assert movie.awards == 'Test Award'
        assert movie.poster == 'http://example.com/poster.jpg'
        assert movie.metascore == 80
        assert movie.imdb_rating == 7.5
        assert movie.imdb_votes == '1000'
        assert movie.imdb_id == 'tt1234567'
        assert movie.type == OmdbResultType.MOVIE
        assert movie.dvd == '2022-05-01'
        assert movie.box_office == '$10 million'
        assert movie.production == 'Test Production'
        assert movie.website == 'http://example.com'
        assert movie.response is True

    def test_movie_model_validation_invalid_data(self, movie_data):
        _movie_data = copy(movie_data)
        _movie_data['metascore'] = 'invalid'
        with pytest.raises(DataError):
            Movie(**_movie_data).save()

    def test_movie_model_validation_invalid_string_length(self, movie_data):
        # NOTE: SQLite doesn't enforce string length conditions
        _movie_data = copy(movie_data)
        _movie_data['year'] = '202412'
        with pytest.raises(DataError):
            Movie(**_movie_data).save()

    def test_movie_model_relationship(self, movie_data):
        movie = Movie(**movie_data)
        movie.save()

        rating1 = Rating(source='IMDb', value='8.0', movie_id=movie.id)
        rating2 = Rating(source='Rotten Tomatoes', value='90%', movie_id=movie.id)
        movie.ratings = [rating1, rating2]
        movie.save()

        assert len(movie.ratings) == 2
        assert movie.ratings[0].value == '8.0'
        assert movie.ratings[1].value == '90%'

    def test_movie_model_database_interaction(self, movie_data):
        movie = Movie(**movie_data)
        movie.save()

        retrieved_movie = Movie.one_or_none(imdb_id='tt1234567')
        assert retrieved_movie.title == 'Test Movie'
        assert retrieved_movie.year == '2022'
        movie.delete()

    def test_movie_model_update(self, movie_data):
        movie = Movie(**movie_data)
        movie.save()

        movie.title = 'Updated Title'
        movie.save()

        updated_movie = Movie.one_or_none(imdb_id='tt1234567')
        assert updated_movie.title == 'Updated Title'
        movie.delete()

    def test_movie_model_deletion(self, movie_data):
        movie = Movie(**movie_data)
        movie.save()

        movie.delete()

        deleted_movie = Movie.one_or_none(imdb_id='tt1234567')
        assert deleted_movie is None

    def test_movie_model_deletion_cascade_ratings(self, movie_data):
        movie = Movie(**movie_data).save()
        rating = Rating(source='IMDb', value='8.0', movie_id=movie.id).save()
        movie.ratings = [rating]
        movie.save()

        movie.delete()

        deleted_movie = Movie.one_or_none(imdb_id='tt1234567')
        assert deleted_movie is None

        deleted_rating = Rating.one_or_none(movie_id=movie.id)
        assert deleted_rating is None
