# -*- coding: utf-8 -*-

from flask import Response

from tests.conftest import BaseTest


class TestUserLoginView(BaseTest):
    ENDPOINT = '/api/%s'

    def test_login_success(self):
        response = self.client.get(self.ENDPOINT % 'login')
        assert response.status_code == 200

    def test_login_invalid_email(self):
        response = self.client.post(
            self.ENDPOINT % 'login',
            data={'email': 'invalid_email', 'password': 'password', 'csrf_token': self.csrf_token},
        )
        assert response.status_code == 400
        assert 'Invalid email' in response.get_data(as_text=True)

    def test_login_invalid_credentials(self):
        response = self.client.post(
            self.ENDPOINT % 'login', data={'email': 'valid_email@example.com', 'password': 'wrong_password'}
        )
        assert response.status_code == 400
        assert 'Invalid email or password' in response.get_data(as_text=True)

    def test_login_valid_credentials(self):
        response = self.client.post(
            self.ENDPOINT % 'login', data={'email': 'valid_email@example.com', 'password': 'valid_password'}
        )
        assert response.status_code == 200
        assert isinstance(response, Response)
        # Add more assertions as needed
