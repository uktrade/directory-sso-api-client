from unittest import TestCase, mock

from tests import stub_request

from directory_sso_api_client.user import UserAPIClient


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
            cache_control=None,
            cookies=None,
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
            cookies=None,
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
            cookies=None,
        )

    @stub_request('https://example.com/api/v1/session-user/', 'get')
    def test_get_session_user_w_cookies(self, stub):
        cookies = {'which_cookie': 'tasty_cookie'}
        self.client.get_session_user(session_id=1, cookies=cookies)

        request = stub.request_history[0]
        assert request.headers['Cookie'] == 'which_cookie=tasty_cookie'

    @stub_request('https://example.com/api/v1/password-check/', 'post')
    def test_check_password_w_cookies(self, stub):
        cookies = {'which_cookie': 'tasty_cookie'}
        self.client.check_password(
            session_id=123, password='my password', cookies=cookies
        )

        request = stub.request_history[0]
        assert request.headers['Cookie'] == 'which_cookie=tasty_cookie'

    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_check_password_call_w_cookies(self, mocked_request):
        cookies = {'which_cookie': 'tasty_cookie'}
        self.client.check_password(
            session_id=123, password='my password', cookies=cookies
        )

        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            content_type='application/json',
            data='{"session_key": 123, "password": "my password"}',
            method='POST',
            url='api/v1/password-check/',
            authenticator=None,
            cookies=cookies,
        )
