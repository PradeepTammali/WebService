# -*- coding: utf-8 -*-
from omdb.models.user import User
from tests.conftest import BaseTest


class TestUserRegisterView(BaseTest):
    ENDPOINT = '/api/register'

    def test_register_success(self):
        response = self.client.get(self.ENDPOINT)
        assert response.status_code == 200

    def test_register_invalid_email(self):
        user = User(email='valid_email@example.com', password='valid_password').save()  # noqa: S106
        response = self.client.post(
            self.ENDPOINT,
            data={'email': user.email, 'password': 'password', 'cpassword': 'password'},
            headers={'Content-Type': 'multipart/form-data'},
        )
        assert response.status_code == 400
        assert 'Invalid email or password' in response.get_data(as_text=True)

    def test_register(self):
        response = self.client.post(
            self.ENDPOINT,
            data={'email': 'valid_email@example.com', 'password': 'valid_password', 'cpassword': 'valid_password'},
            headers={'Content-Type': 'multipart/form-data'},
        )
        assert response.status_code == 200
        data = response.json
        assert data['email'] == 'valid_email@example.com'
        assert data['is_admin'] is False
