from unittest import TestCase

from directory_sso_api_client.client import DirectorySSOAPIClient
from directory_sso_api_client.user import UserAPIClient

from tests import stub_request


class DirectorySSOAPIClientTest(TestCase):

    def setUp(self):
        self.base_url = 'https://example.com'
        self.api_key = 'test'
        self.client = DirectorySSOAPIClient(
            base_url=self.base_url,
            api_key=self.api_key,
            sender_id='test',
            timeout=5,
        )

    def test_user(self):
        assert isinstance(self.client.user, UserAPIClient)
        assert self.client.user.base_url == self.base_url
        assert self.client.user.request_signer.secret == self.api_key

    def test_endpoints_urljoin(self):
        """urljoin replaces base_url's path if endpoints start with with / """
        for endpoint in self.client.user.endpoints.values():
            assert not endpoint.startswith('/')

    @stub_request('https://example.com/api/v1/healthcheck/ping/', 'get')
    def test_health_check(self, stub):
        self.client.ping()

        request = stub.request_history[0]
        assert request
