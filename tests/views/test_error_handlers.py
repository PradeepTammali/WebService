# -*- coding: utf-8 -*-
from tests.conftest import BaseTest


class TestErrorHandlers(BaseTest):
    def test_error_500(self):
        response = self.client.get('/api/error_handlers/internal_error')
        assert response.status_code == 500
        assert response.json == {'error': 'Internal server error', 'status_code': 500}

        response = self.client.get('/api/error_handlers/internal_error2')
        assert response.status_code == 500
        assert response.json == {'error': 'Internal server error', 'status_code': 500}

    def test_error_404(self) -> None:
        response = self.client.get('/api/error_handlers/missing_path')
        assert response.status_code == 404
        assert response.json == {'error': 'Not found', 'status_code': 404}

        response = self.client.get('/api/error_handlers/missing_path2')
        assert response.status_code == 404
        assert response.json == {'error': 'The page you are trying to reach does not exist', 'status_code': 404}

    def test_error_403(self) -> None:
        response = self.client.get('/api/error_handlers/forbidden')
        assert response.status_code == 403
        assert response.json == {'error': 'Forbidden', 'status_code': 403}

    def test_error_400(self):
        response = self.client.get('/api/error_handlers/invalid')
        assert response.status_code == 400
        assert response.json == {'error': 'The data you supplied is not accepted', 'status_code': 400}

        response = self.client.get('/api/error_handlers/invalid2')
        assert response.status_code == 400
        assert response.json == {'error': 'The data you supplied is not accepted', 'status_code': 400}

    def test_error_405(self):
        response = self.client.get('/api/error_handlers/method_not_allowed')
        assert response.status_code == 405
        assert response.json == {'error': 'The method is not allowed for the requested URL.', 'status_code': 405}

    def test_error_429(self):
        response = self.client.get('/api/error_handlers/too_many_requests')
        assert response.status_code == 429
        assert response.json == {'error': 'Too many requests', 'status_code': 429}

    def test_error_401(self):
        response = self.client.get('/api/error_handlers/unauthorized')
        assert response.status_code == 401
        assert response.json == {'error': 'Unauthorized', 'status_code': 401}
