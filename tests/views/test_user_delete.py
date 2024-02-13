# -*- coding: utf-8 -*-

from tests.conftest import BaseTest


class TestUserLoginView(BaseTest):
    ENDPOINT = '/api/delete/%s'

    def test_user_delete_no_logged_in_user(self):
        response = self.client.json_delete(self.ENDPOINT % 1)
        assert response.status_code == 302

    def test_user_delete_not_fresh_login(self):
        user = self.login_as_user()
        response = self.client.json_delete(self.ENDPOINT % user.id)
        assert response.status_code == 401

    def test_user_delete_not_admin(self):
        user = self.login_as_user(fresh=True)
        response = self.client.json_delete(self.ENDPOINT % user.id)
        assert response.status_code == 400
        assert response.json == {'error': 'Invalid user', 'status_code': 400}

    def test_user_delete_admin_not_fresh_login(self):
        admin_user = self.login_as_user(admin=True)
        response = self.client.json_delete(self.ENDPOINT % admin_user.id)
        assert response.status_code == 401
