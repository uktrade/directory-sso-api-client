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
        email = 'test@example.com'
        response = self.client.get_user_by_email(email=email)
        request = stub.request_history[0]
        assert request.url == response.url

    @stub_request(url + 'None/', 'get', 404)
    def test_get_user_should_return_404_on_missing_email(self, stub):
        response = self.client.get_user_by_email(email=None)
        assert response.status_code == 404

    @stub_request(url, 'get', 404)
    def test_get_user_should_return_404_on_empty_email(self, stub):
        response = self.client.get_user_by_email(email='')
        assert response.status_code == 404

    @mock.patch('directory_sso_api_client.base.BaseAPIClient.request')
    def test_get_user_should_make_request_on_empty_email(self, mocked_request):
        self.client.get_user_by_email(email='')
        assert mocked_request.call_count == 1

    @mock.patch('directory_sso_api_client.base.BaseAPIClient.request')
    def test_get_user_should_make_request_on_no_email(self, mocked_request):
        self.client.get_user_by_email(email=None)
        assert mocked_request.call_count == 1

    @mock.patch('directory_sso_api_client.base.BaseAPIClient.request')
    def test_get_user_by_mail_check_request_parameters(self, mocked_request):
        email = 'test@user.com'
        self.client.get_user_by_email(email=email)

        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            method='GET', params=None,
            url='testapi/user-by-email/{}/'.format(email), headers=None,
        )

    @stub_request(url + 'test@example.com/', 'delete')
    def test_delete_user_by_email(self, stub):
        email = 'test@example.com'
        response = self.client.delete_user_by_email(email=email)
        request = stub.request_history[0]
        assert request.url == response.url

    @stub_request(url + 'None/', 'delete', 404)
    def test_delete_user_should_return_404_on_missing_email(self, stub):
        response = self.client.delete_user_by_email(email=None)
        assert response.status_code == 404

    @stub_request(url, 'delete', 404)
    def test_delete_user_should_return_404_on_empty_email(self, stub):
        response = self.client.delete_user_by_email(email='')
        assert response.status_code == 404

    @mock.patch('directory_sso_api_client.base.BaseAPIClient.request')
    def test_delete_user_should_make_request_on_empty_email(
            self, mocked_request):
        self.client.delete_user_by_email(email='')
        assert mocked_request.call_count == 1

    @mock.patch('directory_sso_api_client.base.BaseAPIClient.request')
    def test_delete_user_should_make_request_on_no_email(
            self, mocked_request):
        self.client.delete_user_by_email(email=None)
        assert mocked_request.call_count == 1

    @mock.patch('directory_sso_api_client.base.BaseAPIClient.request')
    def test_delete_user_check_request_arguments(self, mocked_request):
        email = 'test@user.com'
        self.client.delete_user_by_email(email=email)

        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            method='DELETE',
            url='testapi/user-by-email/{}/'.format(email)
        )

    @stub_request(url + 'test@example.com/', 'patch')
    def test_flag_user_email_as_verified_or_not(self, stub):
        email = 'test@example.com'
        response = self.client.flag_user_email_as_verified_or_not(email, True)
        request = stub.request_history[0]
        assert request.url == response.url

    @stub_request(url + 'None/', 'patch', 404)
    def test_flag_user_should_return_404_on_no_email(self, stub):
        response = self.client.flag_user_email_as_verified_or_not(email=None, verified=True)
        assert response.status_code == 404

    @stub_request(url, 'patch', 404)
    def test_flag_user_should_return_404_on_empty_email(self, stub):
        response = self.client.flag_user_email_as_verified_or_not(email='', verified=False)
        assert response.status_code == 404

    @mock.patch('directory_sso_api_client.base.BaseAPIClient.request')
    def test_flag_user_should_make_request_on_empty_email(
            self, mocked_request):
        self.client.flag_user_email_as_verified_or_not(email='', verified=True)
        assert mocked_request.call_count == 1

    @mock.patch('directory_sso_api_client.base.BaseAPIClient.request')
    def test_flag_user_should_make_request_on_no_email(
            self, mocked_request):
        self.client.flag_user_email_as_verified_or_not(email=None, verified=True)
        assert mocked_request.call_count == 1

    @mock.patch('directory_sso_api_client.base.BaseAPIClient.request')
    def test_flag_user_check_request_arguments(self, mocked_request):
        email = 'test@user.com'
        self.client.flag_user_email_as_verified_or_not(email=email, verified=True)
        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            method='PATCH',
            url='testapi/user-by-email/{}/'.format(email),
            data='{"is_verified": true}',
            content_type='application/json'
        )
