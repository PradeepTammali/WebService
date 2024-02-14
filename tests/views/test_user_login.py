# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, patch

from omdb.models.user import User
from tests.conftest import BaseTest


class TestUserLoginView(BaseTest):
    ENDPOINT = '/api/%s'

    def test_login_success(self):
        response = self.client.get(self.ENDPOINT % 'login')
        assert response.status_code == 200

    def test_login_invalid_email(self):
        response = self.client.post(
            self.ENDPOINT % 'login',
            data={'email': 'invalid-email@test.com', 'password': 'password'},
            headers={'Content-Type': 'multipart/form-data'},
        )
        assert response.status_code == 400
        assert 'Invalid email' in response.get_data(as_text=True)

    def test_login_invalid_credentials(self):
        user = User(email='valid_email@example.com', password='valid_password').save()  # noqa: S106
        response = self.client.post(
            self.ENDPOINT % 'login',
            data={'email': user.email, 'password': 'wrong_password'},
            headers={'Content-Type': 'multipart/form-data'},
        )
        assert response.status_code == 400
        assert 'Invalid email or password' in response.get_data(as_text=True)

    @patch('omdb.controllers.user.user_login.login_user')
    def test_login_user_login_failed(self, mock_login_user: MagicMock):
        mock_login_user.return_value = False
        user = User(email='valid_email@example.com', password='valid_password').save()  # noqa: S106
        response = self.client.post(
            self.ENDPOINT % 'login',
            data={'email': user.email, 'password': 'valid_password'},
            headers={'Content-Type': 'multipart/form-data'},
        )
        assert response.status_code == 400

    def test_login_valid_credentials(self):
        user = User(email='valid_email@example.com', password='valid_password').save()  # noqa: S106
        user_id = user.id
        response = self.client.post(
            self.ENDPOINT % 'login',
            data={'email': user.email, 'password': 'valid_password'},
            headers={'Content-Type': 'multipart/form-data'},
        )
        assert response.status_code == 200
        data = response.json
        assert data['email'] == 'valid_email@example.com'
        assert data['id'] == user_id
