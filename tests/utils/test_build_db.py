# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, patch

from omdb.exceptions.base import OmdbInvalidDataException
from omdb.models.movie import Movie, Rating
from omdb.utils.build_db import DATASET_SIZE, _dump_data_to_db, _get_movie_imdb_ids, _get_movies_data, populate_database
from tests.conftest import BaseTest


def mock_search(page):
    return {
        'Search': [
            {
                'Title': 'The Avengers',
                'Year': '2012',
                'imdbID': f'tt0848228{page}{i}',
                'Type': 'movie',
                'Poster': 'https://m.media-amazon.com/images/M/MV5BNDYxNjQyMjAtNTdiOS00NGYwLWFmNTAtNThmYjU5ZGI2YTI1XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg',
            }
            for i in range(10)
        ],
        'totalResults': '119',
        'Response': 'True',
    }


def mock_get_by_imdb_id(imdb_id):
    return {
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
        'imdbID': f'{imdb_id}',
        'Type': 'movie',
        'DVD': '30 Jul 2019',
        'BoxOffice': '$858,373,000',
        'Production': 'N/A',
        'Website': 'N/A',
        'Response': 'True',
    }


@patch('omdb.utils.request.OmdbRequest.get_by_imdb_id')
@patch('omdb.utils.request.OmdbRequest.search')
class TestPopulateDatabase(BaseTest):
    def test_get_movie_imdb_ids_failed(self, mock_omdb_api_search: MagicMock, _):
        mock_omdb_api_search.reset_mock()
        mock_omdb_api_search.return_value = {
            'Search': [
                {
                    'Title': 'The Avengers',
                    'Year': '2012',
                    'imdbID': 'tt0848228',
                    'Type': 'movie',
                    'Poster': 'https://m.media-amazon.com/images/M/MV5BNDYxNjQyMjAtNTdiOS00NGYwLWFmNTAtNThmYjU5ZGI2YTI1XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg',
                },
            ],
            'totalResults': '10',
            'Response': 'True',
        }
        with self.assert_raises(OmdbInvalidDataException):
            _get_movie_imdb_ids()

    def test_get_movie_imdb_ids(self, mock_omdb_api_search: MagicMock, _):
        mock_omdb_api_search.side_effect = mock_search
        imdb_ids = _get_movie_imdb_ids()

        assert len(imdb_ids) == DATASET_SIZE
        assert all(isinstance(imdb_id, str) for imdb_id in imdb_ids)
        mock_omdb_api_search.assert_called()
        assert mock_omdb_api_search.call_count == 10

    def test_get_movies_data(self, mock_omdb_api_search: MagicMock, mock_omdb_api_get_by_imdb_id: MagicMock):
        mock_omdb_api_search.side_effect = mock_search
        mock_omdb_api_get_by_imdb_id.side_effect = mock_get_by_imdb_id
        imdb_ids = _get_movie_imdb_ids()
        movies_data = _get_movies_data(imdb_ids)

        assert len(movies_data) == DATASET_SIZE
        assert all(isinstance(movie, dict) for movie in movies_data)
        mock_omdb_api_search.assert_called()
        assert mock_omdb_api_search.call_count == 10
        mock_omdb_api_get_by_imdb_id.assert_called()
        assert mock_omdb_api_get_by_imdb_id.call_count == 100

    def test_dump_data_to_db(self, mock_omdb_api_search: MagicMock, mock_omdb_api_get_by_imdb_id: MagicMock):
        mock_omdb_api_search.side_effect = mock_search
        mock_omdb_api_get_by_imdb_id.side_effect = mock_get_by_imdb_id
        imdb_ids = _get_movie_imdb_ids()
        movies_data = _get_movies_data(imdb_ids)
        _dump_data_to_db(movies_data)

        assert Movie.count() == DATASET_SIZE
        assert Rating.count() == 300
        mock_omdb_api_search.assert_called()
        assert mock_omdb_api_search.call_count == 10
        mock_omdb_api_get_by_imdb_id.assert_called()
        assert mock_omdb_api_get_by_imdb_id.call_count == 100

    @patch('omdb.utils.build_db._dump_data_to_db')
    @patch('omdb.config.base.BaseConfig.is_unittest')
    def test_populate_database_failed(
        self,
        mock_is_unittest: MagicMock,
        mock_dump_data_to_db: MagicMock,
        mock_omdb_api_search: MagicMock,
        mock_omdb_api_get_by_imdb_id: MagicMock,
        test_app,
    ):
        mock_dump_data_to_db.side_effect = Exception
        mock_is_unittest.return_value = False
        mock_omdb_api_search.side_effect = mock_search
        mock_omdb_api_get_by_imdb_id.side_effect = mock_get_by_imdb_id

        with self.assert_raises(SystemExit):
            populate_database(app=test_app)
        mock_dump_data_to_db.assert_called()
        assert mock_dump_data_to_db.call_count == 1
        mock_is_unittest.assert_called()
        assert mock_is_unittest.call_count == 1
        mock_omdb_api_search.assert_called()
        assert mock_omdb_api_search.call_count == 10
        mock_omdb_api_get_by_imdb_id.assert_called()
        assert mock_omdb_api_get_by_imdb_id.call_count == 100

    @patch('omdb.config.base.BaseConfig.is_unittest')
    def test_populate_database(
        self,
        mock_is_unittest: MagicMock,
        mock_omdb_api_search: MagicMock,
        mock_omdb_api_get_by_imdb_id: MagicMock,
        test_app,
    ):
        mock_is_unittest.return_value = False
        mock_omdb_api_search.side_effect = mock_search
        mock_omdb_api_get_by_imdb_id.side_effect = mock_get_by_imdb_id

        populate_database(app=test_app)
        assert Movie.count() == DATASET_SIZE
        assert Rating.count() == 300

        mock_is_unittest.assert_called()
        assert mock_is_unittest.call_count == 1
        mock_omdb_api_search.assert_called()
        assert mock_omdb_api_search.call_count == 10
        mock_omdb_api_get_by_imdb_id.assert_called()
        assert mock_omdb_api_get_by_imdb_id.call_count == 100

        populate_database(app=test_app)
        assert mock_is_unittest.call_count == 2
        assert mock_omdb_api_search.call_count == 10
        assert mock_omdb_api_get_by_imdb_id.call_count == 100
