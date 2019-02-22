from collections import OrderedDict
import json
from unittest import TestCase, mock

from directory_sso_api_client.user import UserAPIClient

from tests import stub_request


class UserAPIClientTest(TestCase):

    def setUp(self):
        self.client = UserAPIClient(
            base_url='https://example.com',
            api_key='test-api-key',
            sender_id='test',
            timeout=5,
        )

    @stub_request('https://example.com/api/v1/session-user/', 'get')
    def test_get_session_user(self, stub):
        self.client.get_session_user(session_id=1)

    @stub_request('https://example.com/oauth2/user-profile/v1/', 'get')
    def test_get_oauth2_user_profile(self, stub):
        self.client.get_oauth2_user_profile('123')

        request = stub.request_history[0]
        assert request.headers['Authorization'] == 'Bearer 123'

    @stub_request('https://example.com/api/v1/last-login/', 'get')
    def test_get_last_login(self, stub):
        self.client.get_last_login()

    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_get_last_login_with_params(self, mocked_request):
        params = {'start': '2016-11-01', 'end': '2016-11-11'}

        self.client.get_last_login(**params)

        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            method='GET',
            params=params,
            url='api/v1/last-login/',
            authenticator=None,
            cache_control=None
        )

    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_get_last_login_without_params(self, mocked_request):
        self.client.get_last_login()

        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            method='GET',
            params=None,
            url='api/v1/last-login/',
            authenticator=None,
            cache_control=None,
        )

    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_check_password(self, mocked_request):
        self.client.check_password(
            session_id=123, password='my password'
        )

        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            content_type='application/json',
            data='{"session_key": 123, "password": "my password"}',
            method='POST',
            url='api/v1/password-check/',
            authenticator=None,
        )

    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_regenerate_verification_code(self, mocked_request):

        self.client.regenerate_verification_code('test@test1234.com')

        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            content_type='application/json',
            data='{"email": "test@test1234.com"}',
            method='POST',
            url='api/v1/verification-code/regenerate/',
            authenticator=None,
        )

    @mock.patch('directory_client_core.authentication.SessionSSOAuthenticator')
    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_verify_verification_code(
        self, mocked_request, mocked_authenticator
    ):
        data = OrderedDict([
            ('code', '12345'),
            ('email', 'test@example.com'),
        ])

        self.client.verify_verification_code(data)
        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            content_type='application/json',
            data='{"code": "12345", "email": "test@example.com"}',
            method='POST',
            url='api/v1/verification-code/verify/',
            authenticator=None,
        )

    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_create_user(self, mocked_request):
        self.client.create_user(
            email='test@testuser.com',
            password='mypassword'
        )

        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            content_type='application/json',
            data='{"email": "test@testuser.com", "password": "mypassword"}',
            method='POST',
            url='api/v1/user/',
            authenticator=None,
        )

    @mock.patch('directory_client_core.authentication.SessionSSOAuthenticator')
    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_create_user_profile(self, mocked_request, mocked_authenticator):

        user_profile_data = {
            'first_name': 'john',
            'last_name': 'smith',
            'job_title': 'director',
            'mobile_phone_number': '0788712738738',
        }

        self.client.create_user_profile(
            sso_session_id=999,
            data=user_profile_data
        )
        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            content_type='application/json',
            method='POST',
            data=json.dumps(user_profile_data),
            url='api/v1/user/profile/',
            authenticator=mocked_authenticator(),
        )
