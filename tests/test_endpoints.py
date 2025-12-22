import pytest


class TestHealthEndpoint:

    def test_health_returns_ok(self, client):
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'

    def test_health_returns_json(self, client):
        response = client.get('/health')
        assert response.content_type == 'application/json'


class TestRootEndpoint:

    def test_root_returns_service_info(self, client):
        response = client.get('/')
        assert response.status_code == 200
        data = response.get_json()
        assert data['service'] == 'BlueLabel DevOps API'

    def test_root_lists_endpoints(self, client):
        response = client.get('/')
        data = response.get_json()
        assert '/health' in data['endpoints']
        assert '/info' in data['endpoints']


class TestInfoEndpoint:

    def test_info_returns_json(self, client):
        response = client.get('/info')
        assert response.content_type == 'application/json'
