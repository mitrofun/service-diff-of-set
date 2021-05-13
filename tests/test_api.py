from starlette.testclient import TestClient

from src.main import app

client = TestClient(app)


class TestListCalculation:

    url = '/calculations'

    def test_without_key(self):
        response = client.get(self.url)
        assert response.status_code == 403
        assert response.json() == {'detail': 'Not authenticated'}

    def test_with_key(self):
        response = client.get(self.url, headers={'X-API-KEY': 'test-key'})
        assert response.status_code == 200


class TestDetailCalculation:

    def test_invalid_id(self):
        response = client.get('/calculations/1000', headers={'X-API-KEY': 'test-key'})
        assert response.status_code == 404
