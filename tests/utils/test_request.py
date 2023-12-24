# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, patch

from omdb.exceptions.base import OmdbRequestException
from omdb.utils.request import OmdbRequest
from tests.conftest import BaseTest


class TestOmdbRequest(BaseTest):
    def test_init(self):
        test_kwargs = {
            'supported_methods': ['GET', 'POST'],
            'base_url': 'https://sample.com',
            'headers': {'Accept': 'application/json'},
            'log_response_codes': [500],
            'session': True,
            'request_json': True,
        }
        test_request = OmdbRequest(**test_kwargs)
        assert test_request.request_supported_methods == test_kwargs['supported_methods']
        assert test_request.request_base_url == test_kwargs['base_url']
        assert test_request.request_headers == test_kwargs['headers']
        assert test_request.request_log_response_codes == test_kwargs['log_response_codes']
        assert test_request.request_session == test_kwargs['session']
        assert test_request.request_json == test_kwargs['request_json']

    def test_unsupported_method(self):
        omdb_request = OmdbRequest(supported_methods=['POST'])
        with self.assert_raises(OmdbRequestException):
            omdb_request.search(page=1)

    @patch('omdb.utils.request.requests.Session.get')
    def test_request_json(self, mock_get: MagicMock):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'Search': [{'Title': 'The Avengers', 'Year': '2012', 'imdbID': 'tt123456', 'Type': 'movie'}]
        }
        omdb_request = OmdbRequest()
        result = omdb_request.search(page=1, data={'sample': 'data'})
        assert 'Search' in result

    @patch('omdb.utils.request.requests.Session.get')
    def test_response_none(self, mock_get: MagicMock):
        mock_get.return_value = None
        omdb_request = OmdbRequest()
        with self.assert_raises(OmdbRequestException):
            omdb_request.search(page=1)

    @patch('omdb.utils.request.requests.Session.get')
    def test_search_successful(self, mock_get: MagicMock):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'Search': [{'Title': 'The Avengers', 'Year': '2012', 'imdbID': 'tt123456', 'Type': 'movie'}]
        }
        omdb_request = OmdbRequest()
        result = omdb_request.search(page=1)
        assert 'Search' in result

    @patch('omdb.utils.request.requests.Session.get')
    def test_search_failure(self, mock_get: MagicMock):
        mock_get.return_value.status_code = 500
        mock_get.return_value.text = 'Internal Server Error'
        omdb_request = OmdbRequest()
        with self.assert_raises(OmdbRequestException):
            omdb_request.search(page=1)

    @patch('omdb.utils.request.requests.Session.get')
    def test_get_by_imdb_id_successful(self, mock_get: MagicMock):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'Title': 'The Avengers',
            'Year': '2012',
            'imdbID': 'tt123456',
            'Type': 'movie',
        }
        omdb_request = OmdbRequest()
        result = omdb_request.get_by_imdb_id(imdb_id='tt123456')
        assert result['imdbID'] == 'tt123456'

    @patch('omdb.utils.request.requests.Session.get')
    def test_get_by_imdb_id_failure(self, mock_get: MagicMock):
        mock_get.return_value.status_code = 403
        mock_get.return_value.text = 'Forbidden'
        omdb_request = OmdbRequest()
        with self.assert_raises(OmdbRequestException):
            omdb_request.get_by_imdb_id(imdb_id='tt123456')
