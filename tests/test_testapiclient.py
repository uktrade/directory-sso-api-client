from unittest import TestCase, mock

from directory_sso_api_client.testapiclient import DirectoryTestAPIClient

from tests import stub_request


class DirectoryTestAPIClientTest(TestCase):

    url = 'https://example.com/testapi/user-by-email/'

    def setUp(self):
        self.base_url = 'https://example.com'
        self.api_key = 'test'
        self.client = DirectoryTestAPIClient(self.base_url, self.api_key)

    def test_endpoints_urljoin(self):
        """urljoin replaces base_url's path if endpoints start with with / """
        for endpoint in self.client.endpoints.values():
            assert not endpoint.startswith('/')

    @stub_request(url + 'test@example.com/', 'get')
    def test_get_user_by_email(self, stub):
        email = "test@example.com"
        response = self.client.get_user_by_email(email=email)
        request = stub.request_history[0]
        assert request.url == response.url

    def test_should_return_none_on_missing_email(self):
        response = self.client.get_user_by_email(email=None)
        assert response is None

    def test_should_return_none_on_empty_email(self):
        response = self.client.get_user_by_email(email="")
        assert response is None

    @mock.patch('directory_sso_api_client.base.BaseAPIClient.request')
    def test_should_not_make_any_request_on_empty_email(self, mocked_request):
        self.client.get_user_by_email(email="")
        assert mocked_request.call_count == 0

    @mock.patch('directory_sso_api_client.base.BaseAPIClient.request')
    def test_should_not_make_any_request_on_no_email(self, mocked_request):
        self.client.get_user_by_email(email=None)
        assert mocked_request.call_count == 0

    @mock.patch('directory_sso_api_client.base.BaseAPIClient.request')
    def test_get_last_login_without_params(self, mocked_request):
        email = "test@user.com"
        self.client.get_user_by_email(email=email)

        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            method='GET', params=None,
            url='testapi/user-by-email/{}/'.format(email), headers=None,
        )
