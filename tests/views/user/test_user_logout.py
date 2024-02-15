# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, patch

from tests.conftest import BaseTest


class TestUserLogoutView(BaseTest):
    ENDPOINT = '/api/logout'

    def test_logout_not_logged(self):
        response = self.client.get(self.ENDPOINT)
        assert response.status_code == 302

    @patch('omdb.views.user.user_logout.logout_user')
    def test_logout_user_logout_failed(self, mock_logout_user: MagicMock):
        self.login_as_user()

        mock_logout_user.return_value = False
        response = self.client.get(self.ENDPOINT)
        assert response.status_code == 400

    def test_logout_success(self):
        self.login_as_user()

        response = self.client.get(self.ENDPOINT)
        assert response.status_code == 302
