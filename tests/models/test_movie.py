# -*- coding: utf-8 -*-
import datetime

import pytest

from omdb.models.movie import Movie, Rating
from tests.conftest import BaseTest

# TODO: have this as a fixture
movie_data = {
    'title': 'Test Movie',
    'year': '2022',
    'rated': 'PG',
    'released': '2022-01-01',
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
    'metascore': '80',
    'imdb_rating': '7.5',
    'imdb_votes': '1000',
    'imdb_id': 'tt1234567',
    'type_': 'movie',
    'dvd': '2022-05-01',
    'box_office': '$10 million',
    'production': 'Test Production',
    'website': 'http://example.com',
    'response': 'True',
}


class TestRatingDatabase(BaseTest):
    def test_rating_model_creation(self):
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

    def test_rating_model_str_representation(self):
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
    def test_movie_model_initialization(self):
        movie = Movie(**movie_data)
        movie.save()

        assert movie.class_name == Movie.__name__
        assert movie.id
        assert isinstance(movie.created, datetime.datetime)
        assert isinstance(movie.updated, datetime.datetime)
        assert movie.title == 'Test Movie'
        assert movie.year == '2022'
        assert movie.rated == 'PG'
        assert movie.released == '2022-01-01'
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
        assert movie.metascore == '80'
        assert movie.imdb_rating == '7.5'
        assert movie.imdb_votes == '1000'
        assert movie.imdb_id == 'tt1234567'
        assert movie.type == 'movie'
        assert movie.dvd == '2022-05-01'
        assert movie.box_office == '$10 million'
        assert movie.production == 'Test Production'
        assert movie.website == 'http://example.com'
        assert movie.response == 'True'

    def test_movie_model_validation_invalid_data(self):
        with pytest.raises(TypeError):
            Movie(title='Invalid Title', year='2022', imdb_id='tt1234567', imdb_rating='invalid')

    def test_movie_model_relationship(self):
        movie = Movie(**movie_data)
        movie.save()

        rating1 = Rating(source='IMDb', value='8.0', movie_id=movie.id)
        rating2 = Rating(source='Rotten Tomatoes', value='90%', movie_id=movie.id)
        movie.ratings = [rating1, rating2]
        movie.save()

        assert len(movie.ratings) == 2
        assert movie.ratings[0].value == '8.0'
        assert movie.ratings[1].value == '90%'

    def test_movie_model_database_interaction(self):
        movie = Movie(**movie_data)
        movie.save()

        retrieved_movie = Movie.query.filter_by(imdb_id='tt1234567').first()
        assert retrieved_movie.title == 'Test Movie'
        assert retrieved_movie.year == '2022'
        movie.delete()

    def test_movie_model_update(self):
        movie = Movie(**movie_data)
        movie.save()

        movie.title = 'Updated Title'
        movie.save()

        updated_movie = Movie.query.filter_by(imdb_id='tt1234567').first()
        assert updated_movie.title == 'Updated Title'

        movie.delete()

    def test_movie_model_deletion(self):
        movie = Movie(**movie_data)
        movie.save()

        movie.delete()

        deleted_movie = Movie.query.filter_by(imdb_id='tt1234567').first()
        assert deleted_movie is None

    def test_movie_model_deletion_cascade_ratings(self):
        movie = Movie(**movie_data).save()
        rating = Rating(source='IMDb', value='8.0', movie_id=movie.id).save()
        movie.ratings = [rating]
        movie.save()

        self.session.commit()
        movie.delete()

        deleted_movie = Movie.query.filter_by(imdb_id='tt1234567').first()
        assert deleted_movie is None

        deleted_rating = Rating.query.filter_by(movie_id=movie.id).first()
        assert deleted_rating is None
