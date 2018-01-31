from unittest import TestCase

from directory_sso_api_client.testapiclient import DirectoryTestAPIClient

from tests import stub_request


class DirectoryTestAPIClientTest(TestCase):

    endpoint = 'https://example.com/testapi/user-by-email/'

    def setUp(self):
        self.base_url = 'https://example.com'
        self.api_key = 'test'
        self.client = DirectoryTestAPIClient(self.base_url, self.api_key)

    def test_endpoints_urljoin(self):
        """urljoin replaces base_url's path if endpoints start with with / """
        for endpoint in self.client.endpoints.values():
            assert not endpoint.startswith('/')

    @stub_request(endpoint + 'test@example.com/', 'get')
    def test_get_user_by_email(self, stub):
        email = "test@example.com"
        response = self.client.get_user_by_email(email=email, token="debug")
        request = stub.request_history[0]
        assert request.url == response.url

    @stub_request(endpoint + 'test@example.com/', 'get')
    def test_client_should_pass_token(self, stub):
        email = "test@example.com"
        response = self.client.get_user_by_email(email=email, token="debug")
        assert "?token=debug" in response.url

    @stub_request(endpoint + 'test@example.com/', 'get', 404)
    def test_should_return_404_on_wrong_token(self, stub):
        email = "test@example.com"
        response = self.client.get_user_by_email(email=email, token="invalid")
        assert response.status_code == 404

    @stub_request(endpoint + 'test@example.com/', 'get', 404)
    def test_should_return_404_on_missing_token(self, stub):
        email = "test@example.com"
        response = self.client.get_user_by_email(email=email, token=None)
        assert response is None

    def test_should_return_none_on_missing_email(self):
        response = self.client.get_user_by_email(email="", token=None)
        assert response is None

    def test_should_return_none_on_empty_email(self):
        response = self.client.get_user_by_email(email=None, token=None)
        assert response is None

    def test_should_not_pass_empty_token_query_parameter(self):
        email = "test@example.com"
        response = self.client.get_user_by_email(email=email, token=None)
        assert response is None
