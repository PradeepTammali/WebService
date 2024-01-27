# -*- coding: utf-8 -*-
from tests.conftest import BaseTest


class TestValidateSchema(BaseTest):
    def test_get_multiple(self):
        response = self.client.get('/api/test_http/')
        assert response.status_code == 200
        assert 'collection' in response.json
        assert 'count' in response.json
        assert response.json['count'] == 5

    def test_get_missing_required_400(self):
        response = self.client.get('/api/test_http/get')
        assert response.status_code == 400

    def test_get_200(self):
        response = self.client.get('/api/test_http/get?value=foo1&value2=bar1&value3=baz')
        assert response.status_code == 200
        data = response.json
        assert 'id' in data
        assert 'created' in data
        assert 'updated' in data
        assert data['value'] == 'foo1'
        assert data['value2'] == 'bar1'
        assert data['value3'] == 'baz'

    def test_get_one_failed(self):
        response = self.client.get('/api/test_http/get-one/invalid')
        assert response.status_code == 400

        response = self.client.get('/api/test_http/get-one/error')
        assert response.status_code == 500

    def test_get_one_no_data(self):
        response = self.client.get('/api/test_http/get-one/foo1')
        assert response.status_code == 200
        assert not response.json

    def test_get_one_200(self):
        response = self.client.get('/api/test_http/get-one/foo')
        assert response.status_code == 200
        data = response.json
        assert 'id' in data
        assert 'created' in data
        assert 'updated' in data
        assert data['value'] == 'foo'
        assert data['value2'] == 'bar1'
        assert data['value3'] == 'baz'

    def test_post_no_data_400(self):
        response = self.client.post('/api/test_http/post')
        assert response.status_code == 400

        response = self.client.json_post('/api/test_http/post')
        assert response.status_code == 400

    def test_post_200(self):
        response = self.client.json_post(
            '/api/test_http/post', json={'value': 'foo1', 'value2': 'bar1', 'value3': 'baz'}
        )
        assert response.status_code == 200
        data = response.json
        assert 'id' in data
        assert 'created' in data
        assert 'updated' in data
        assert data['value'] == 'foo1'
        assert data['value2'] == 'bar1'
        assert data['value3'] == 'baz'
        assert data['sample_kwargs'] == 'sample_kwargs'
