from unittest import TestCase

from directory_sso_api_client.client import DirectorySSOAPIClient
from directory_sso_api_client.user import UserAPIClient


class DirectorySSOAPIClientTest(TestCase):

    def setUp(self):
        self.base_url = 'https://example.com'
        self.api_key = 'test'
        self.client = DirectorySSOAPIClient(self.base_url, self.api_key)

    def test_user(self):
        assert isinstance(self.client.user, UserAPIClient)
        assert self.client.user.base_url == self.base_url
        assert self.client.user.request_signer.secret == self.api_key

    def test_endpoints_urljoin(self):
        """urljoin replaces base_url's path if endpoints start with with / """
        for endpoint in self.client.user.endpoints.values():
            assert not endpoint.startswith('/')
