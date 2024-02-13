# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, patch

from werkzeug.exceptions import InternalServerError

from omdb.models.user import User
from omdb.request_hooks import load_user
from tests.conftest import BaseTest


class TestRequestHooks(BaseTest):
    ENDPOINT = '/test_request_hooks/'
    ENDPOINT_ERROR = '/test_request_hooks/error'
    ENDPOINT_HEALTH_CHECK = '/api/health_check'

    def test_load_user(self):
        user = load_user('sample@test.com')
        assert not user

        user = User(email='test-user@test.com', password='1234').save()  # noqa: S106
        loaded_user = load_user('test-user@test.com')
        assert loaded_user.id == user.id

    def test_health_check(self):
        response = self.client.get(self.ENDPOINT_HEALTH_CHECK)
        assert response.status_code == 200

        response = self.client.get(self.ENDPOINT_HEALTH_CHECK + '/')
        assert response.status_code == 404

        response = self.client.get(self.ENDPOINT_ERROR)
        assert response.status_code == 404

    @patch('omdb.request_hooks.db.session.commit')
    def test_after_request_commit_failed(self, mock_commit: MagicMock):
        mock_commit.side_effect = Exception('DB commit failed')

        with self.assert_raises(InternalServerError):
            response = self.client.get(self.ENDPOINT)

            mock_commit.assert_called_once()
            self.assert_equal(response.headers['X-Flow-Request-Time'], '0.0f')
            self.assert_in('db commit failed', str(response))

    def test_after_request_commit_success(self):
        with patch('omdb.request_hooks.db.session.commit') as mock_commit:
            response = self.client.get(self.ENDPOINT)

            mock_commit.assert_called_once()
            self.assert_not_in('X-Flow-Request-Time', response.headers)
            self.assert_equal(response, response)
