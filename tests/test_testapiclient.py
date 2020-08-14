from unittest import TestCase, mock

from directory_sso_api_client.testapiclient import DirectorySSOTestAPIClient

from tests import basic_authenticator, stub_request


class DirectorySSOTestAPIClientTest(TestCase):

    url = 'https://example.com/testapi/user-by-email/'

    def setUp(self):
        self.base_url = 'https://example.com'
        self.api_key = 'test'
        self.client = DirectorySSOTestAPIClient(
            base_url=self.base_url,
            api_key=self.api_key,
            sender_id='test',
            timeout=5,
        )

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

    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_get_user_should_make_request_on_empty_email(self, mocked_request):
        self.client.get_user_by_email(email='')
        assert mocked_request.call_count == 1

    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_get_user_should_make_request_on_no_email(self, mocked_request):
        self.client.get_user_by_email(email=None)
        assert mocked_request.call_count == 1

    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_get_user_by_mail_check_request_parameters(self, mocked_request):
        email = 'test@user.com'
        self.client.get_user_by_email(email=email)

        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            method='GET',
            params=None,
            url='testapi/user-by-email/{}/'.format(email),
            authenticator=None,
            cache_control=None,
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

    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_delete_user_should_make_request_on_empty_email(
            self, mocked_request):
        self.client.delete_user_by_email(email='')
        assert mocked_request.call_count == 1

    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_delete_user_should_make_request_on_no_email(
            self, mocked_request):
        self.client.delete_user_by_email(email=None)
        assert mocked_request.call_count == 1

    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_delete_user_check_request_arguments(self, mocked_request):
        email = 'test@user.com'
        self.client.delete_user_by_email(email=email)

        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            method='DELETE',
            url='testapi/user-by-email/{}/'.format(email),
            authenticator=None,
            data=None,
        )

    @stub_request(url + 'test@example.com/', 'patch')
    def test_flag_user_email_as_verified_or_not(self, stub):
        email = 'test@example.com'
        response = self.client.flag_user_email_as_verified_or_not(email, True)
        request = stub.request_history[0]
        assert request.url == response.url

    @stub_request(url + 'None/', 'patch', 404)
    def test_flag_user_should_return_404_on_no_email(self, stub):
        response = self.client.flag_user_email_as_verified_or_not(
            email=None, verified=True)
        assert response.status_code == 404

    @stub_request(url, 'patch', 404)
    def test_flag_user_should_return_404_on_empty_email(self, stub):
        response = self.client.flag_user_email_as_verified_or_not(
            email='', verified=False)
        assert response.status_code == 404

    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_flag_user_should_make_request_on_empty_email(
            self, mocked_request):
        self.client.flag_user_email_as_verified_or_not(
            email='', verified=True)
        assert mocked_request.call_count == 1

    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_flag_user_should_make_request_on_no_email(
            self, mocked_request):
        self.client.flag_user_email_as_verified_or_not(
            email=None, verified=True)
        assert mocked_request.call_count == 1

    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_flag_user_check_request_arguments(self, mocked_request):
        email = 'test@user.com'
        self.client.flag_user_email_as_verified_or_not(
            email=email, verified=True)
        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            method='PATCH',
            url='testapi/user-by-email/{}/'.format(email),
            data='{"is_verified": true}',
            content_type='application/json',
            authenticator=None,
        )

    @stub_request(url + 'test@example.com/', 'get')
    def test_get_user_by_email_with_authenticator(self, stub):
        email = 'test@example.com'
        self.client.get_user_by_email(email=email, authenticator=basic_authenticator)
        request = stub.request_history[0]
        assert 'Authorization' in request.headers
        assert request.headers['Authorization'].startswith('Basic ')

    @stub_request(url + 'test@example.com/', 'delete')
    def test_delete_user_by_email_with_authenticator(self, stub):
        email = 'test@example.com'
        self.client.delete_user_by_email(email=email, authenticator=basic_authenticator)
        request = stub.request_history[0]
        assert 'Authorization' in request.headers
        assert request.headers['Authorization'].startswith('Basic ')

    @stub_request(url + 'test@example.com/', 'patch')
    def test_flag_user_email_as_verified_or_not_with_authenticator(self, stub):
        email = 'test@example.com'
        self.client.flag_user_email_as_verified_or_not(
            email, True, authenticator=basic_authenticator
        )
        request = stub.request_history[0]
        assert 'Authorization' in request.headers
        assert request.headers['Authorization'].startswith('Basic ')
