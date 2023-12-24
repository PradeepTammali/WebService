# -*- coding: utf-8 -*-
import datetime

import pytz

from omdb.config.base import DateFormat
from omdb.schema import fields
from omdb.schema.base import ModelSchema
from omdb.schema.build_db import CustomResultSchema, MovieResultSchema, MovieSearchResultSchema
from tests.conftest import BaseTest


class BaseTestCustomResultSchema(ModelSchema, CustomResultSchema):
    field_one = fields.Str()
    field_two = fields.Str(data_key='fieldTwo', required=True)


class TestCustomResultSchema(BaseTest):
    def test_init(self):
        custom_result_schema = BaseTestCustomResultSchema()
        assert custom_result_schema.exclude == ('id', 'created', 'updated')

        custom_result_schema = BaseTestCustomResultSchema(exclude=('field_one',))
        assert custom_result_schema.exclude == ('id', 'created', 'updated', 'field_one')

    def test_on_bind_field(self):
        custom_result_schema = BaseTestCustomResultSchema()
        assert custom_result_schema.fields['field_one'].data_key == 'FieldOne'
        assert custom_result_schema.fields['field_one'].allow_none is True
        assert custom_result_schema.fields['field_two'].data_key == 'fieldTwo'
        assert custom_result_schema.fields['field_two'].allow_none is False

    def test_replace_na_with_none(self):
        custom_result_schema = BaseTestCustomResultSchema()
        data = custom_result_schema.load({'FieldOne': 'N/A', 'fieldTwo': 'two'})
        assert not data['field_one']
        assert data['field_two'] == 'two'


class TestMovieSearchResultSchema(BaseTest):
    def test_schema(self):
        test_data = {
            'Search': [
                {
                    'Title': 'The Avengers',
                    'Year': '2012',
                    'imdbID': 'tt0848228',
                    'Type': 'movie',
                    'Poster': 'https://m.media-amazon.com/images/M/MV5BNDYxNjQyMjAtNTdiOS00NGYwLWFmNTAtNThmYjU5ZGI2YTI1XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg',
                },
                {
                    'Title': 'Avengers: Endgame',
                    'Year': '2019',
                    'imdbID': 'tt4154796',
                    'Type': 'movie',
                    'Poster': 'https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_SX300.jpg',
                },
            ],
            'totalResults': '119',
            'Response': 'True',
        }
        data = MovieSearchResultSchema().load(test_data)
        assert data['total_results'] == 119
        assert isinstance(data['search'], list)
        assert data['search'][0]['title'] == test_data['Search'][0]['Title']
        assert data['search'][0]['year'] == test_data['Search'][0]['Year']
        assert data['search'][0]['imdb_id'] == test_data['Search'][0]['imdbID']
        assert data['search'][0]['type'].value == test_data['Search'][0]['Type']
        assert data['search'][0]['poster'] == test_data['Search'][0]['Poster']

        assert data['search'][1]['title'] == test_data['Search'][1]['Title']
        assert data['search'][1]['year'] == test_data['Search'][1]['Year']
        assert data['search'][1]['imdb_id'] == test_data['Search'][1]['imdbID']
        assert data['search'][1]['type'].value == test_data['Search'][1]['Type']
        assert data['search'][1]['poster'] == test_data['Search'][1]['Poster']


class TestMovieResultSchema(BaseTest):
    def test_schema(self):
        test_data = {
            'Title': 'Avengers: Endgame',
            'Year': '2019',
            'Rated': 'PG-13',
            'Released': '26 Apr 2019',
            'Runtime': '181 min',
            'Genre': 'Action, Adventure, Drama',
            'Director': 'Anthony Russo, Joe Russo',
            'Writer': 'Christopher Markus, Stephen McFeely, Stan Lee',
            'Actors': 'Robert Downey Jr., Chris Evans, Mark Ruffalo',
            'Plot': "After the devastating events of Avengers: Infinity War (2018), the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos' actions and restore balance to the universe.",
            'Language': 'English, Japanese, Xhosa, German',
            'Country': 'United States',
            'Awards': 'Nominated for 1 Oscar. 70 wins & 133 nominations total',
            'Poster': 'https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_SX300.jpg',
            'Ratings': [
                {'Source': 'Internet Movie Database', 'Value': '8.4/10'},
                {'Source': 'Rotten Tomatoes', 'Value': '94%'},
                {'Source': 'Metacritic', 'Value': '78/100'},
            ],
            'Metascore': '78',
            'imdbRating': '8.4',
            'imdbVotes': '1,230,666',
            'imdbID': 'tt4154796',
            'Type': 'movie',
            'DVD': '30 Jul 2019',
            'BoxOffice': '$858,373,000',
            'Production': 'N/A',
            'Website': 'N/A',
            'Response': 'True',
        }
        data = MovieResultSchema().load(test_data)
        assert data['title'] == test_data['Title']
        assert data['year'] == test_data['Year']
        assert data['rated'] == test_data['Rated']
        assert data['released'] == datetime.datetime.strptime(
            test_data['Released'], DateFormat.DD_BB_YYYY.value
        ).replace(tzinfo=pytz.utc)
        assert data['runtime'] == test_data['Runtime']
        assert data['genre'] == test_data['Genre']
        assert data['director'] == test_data['Director']
        assert data['writer'] == test_data['Writer']
        assert data['actors'] == test_data['Actors']
        assert data['plot'] == test_data['Plot']
        assert data['language'] == test_data['Language']
        assert data['country'] == test_data['Country']
        assert data['awards'] == test_data['Awards']
        assert data['poster'] == test_data['Poster']
        assert data['metascore'] == int(test_data['Metascore'])
        assert data['imdb_rating'] == float(test_data['imdbRating'])
        assert data['imdb_votes'] == test_data['imdbVotes']
        assert data['imdb_id'] == test_data['imdbID']
        assert data['type'].value == test_data['Type']
        assert data['dvd'] == test_data['DVD']
        assert data['box_office'] == test_data['BoxOffice']
        assert not data['production']
        assert not data['website']
        assert str(data['response']) == test_data['Response']
        assert isinstance(data['ratings'], list)
        assert data['ratings'][0]['source'] == test_data['Ratings'][0]['Source']
        assert data['ratings'][0]['value'] == test_data['Ratings'][0]['Value']
        assert data['ratings'][1]['source'] == test_data['Ratings'][1]['Source']
        assert data['ratings'][1]['value'] == test_data['Ratings'][1]['Value']
        assert data['ratings'][2]['source'] == test_data['Ratings'][2]['Source']
        assert data['ratings'][2]['value'] == test_data['Ratings'][2]['Value']
