import json
from collections import OrderedDict
from unittest import TestCase, mock

from directory_sso_api_client.user import UserAPIClient
from tests import basic_authenticator, stub_request


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
            method='GET', params=params, url='api/v1/last-login/', authenticator=None, cache_control=None
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
        self.client.check_password(session_id=123, password='my password')

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

        self.client.regenerate_verification_code({"email": "test@test1234.com"})

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
    def test_verify_verification_code(self, mocked_request, mocked_authenticator):
        data = OrderedDict(
            [
                ('code', '12345'),
                ('email', 'test@example.com'),
            ]
        )

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
        self.client.create_user(email='test@testuser.com', password='mypassword', mobile_phone_number='07111176523')

        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            content_type='application/json',
            data='{"email": "test@testuser.com", "password": "mypassword", "mobile_phone_number": "07111176523"}',
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

        self.client.create_user_profile(sso_session_id=999, data=user_profile_data)
        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            content_type='application/json',
            method='POST',
            data=json.dumps(user_profile_data),
            url='api/v1/user/profile/',
            authenticator=mocked_authenticator(),
        )

    @mock.patch('directory_client_core.authentication.SessionSSOAuthenticator')
    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_update_user_profile(self, mocked_request, mocked_authenticator):

        user_profile_data = {
            'first_name': 'john',
            'last_name': 'smith',
            'job_title': 'director',
            'mobile_phone_number': '0788712738738',
        }

        self.client.update_user_profile(sso_session_id=999, data=user_profile_data)
        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            content_type='application/json',
            method='PATCH',
            data=json.dumps(user_profile_data),
            url='api/v1/user/profile/update/',
            authenticator=mocked_authenticator(),
        )

    @mock.patch('directory_client_core.authentication.SessionSSOAuthenticator')
    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_set_user_page_view(self, mocked_request, mocked_authenticator):

        data = {'service': 'great', 'page': 'dashboard'}
        self.client.set_user_page_view(sso_session_id=999, **data)
        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            content_type='application/json',
            method='POST',
            data=json.dumps(data),
            url='api/v1/user/page-view/',
            authenticator=mocked_authenticator(),
        )

    @stub_request('https://example.com/api/v1/user/page-view/', 'get')
    def test_get_user_page_views(self, stub):

        data = {'service': 'great', 'page': 'dashboard'}
        self.client.get_user_page_views(sso_session_id=1, **data)

    @mock.patch('directory_client_core.authentication.SessionSSOAuthenticator')
    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_set_user_lesson_completed(self, mocked_request, mocked_authenticator):

        data = {
            'service': 'great',
            'lesson_page': 'dashboard',
            'lesson': 12,
            "module": 1,
        }
        self.client.set_user_lesson_completed(sso_session_id=999, **data)
        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            content_type='application/json',
            method='POST',
            data=json.dumps(data),
            url='api/v1/user/lesson-completed/',
            authenticator=mocked_authenticator(),
        )

    @stub_request('https://example.com/api/v1/user/lesson-completed/', 'get')
    def test_get_user_lesson_completed(self, stub):

        data = {'service': 'great', 'lesson_page': 'dashboard'}
        self.client.get_user_lesson_completed(sso_session_id=999, **data)

    @mock.patch('directory_client_core.authentication.SessionSSOAuthenticator')
    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_delete_user_lesson_completed(self, mocked_request, mocked_authenticator):

        data = {'service': 'great', 'lesson': '11'}
        self.client.delete_user_lesson_completed(sso_session_id=999, **data)
        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            method='DELETE',
            url='api/v1/user/lesson-completed/',
            authenticator=mocked_authenticator(),
            data=data,
        )

    @stub_request('https://example.com/api/v1/session-user/', 'get')
    def test_get_session_user_with_authenticator(self, stub):
        self.client.get_session_user(session_id=1, authenticator=basic_authenticator)
        request = stub.request_history[0]
        assert 'Authorization' in request.headers
        assert request.headers['Authorization'].startswith('Basic ')

    @stub_request('https://example.com/api/v1/last-login/', 'get')
    def test_get_last_login_with_authenticator(self, stub):
        self.client.get_last_login(authenticator=basic_authenticator)
        request = stub.request_history[0]
        assert 'Authorization' in request.headers
        assert request.headers['Authorization'].startswith('Basic ')

    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_get_last_login_with_params_and_authenticator(self, mocked_request):
        params = {'start': '2016-11-01', 'end': '2016-11-11'}

        self.client.get_last_login(**params, authenticator=basic_authenticator)

        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            method='GET',
            params=params,
            url='api/v1/last-login/',
            cache_control=None,
            authenticator=basic_authenticator,
        )

    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_get_last_login_without_params_but_with_authenticator(self, mocked_request):
        self.client.get_last_login(authenticator=basic_authenticator)

        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            method='GET',
            params=None,
            url='api/v1/last-login/',
            cache_control=None,
            authenticator=basic_authenticator,
        )

    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_check_password_with_authenticator(self, mocked_request):
        self.client.check_password(session_id=123, password='my password', authenticator=basic_authenticator)

        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            content_type='application/json',
            data='{"session_key": 123, "password": "my password"}',
            method='POST',
            url='api/v1/password-check/',
            authenticator=basic_authenticator,
        )

    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_regenerate_verification_code_with_authenticator(self, mocked_request):

        self.client.regenerate_verification_code(
            {"email": "test@test1234.com"},
            authenticator=basic_authenticator,
        )

        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            content_type='application/json',
            data='{"email": "test@test1234.com"}',
            method='POST',
            url='api/v1/verification-code/regenerate/',
            authenticator=basic_authenticator,
        )

    @mock.patch('directory_client_core.authentication.SessionSSOAuthenticator')
    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_verify_verification_code_with_authenticator(self, mocked_request, mocked_authenticator):
        data = OrderedDict(
            [
                ('code', '12345'),
                ('email', 'test@example.com'),
            ]
        )

        self.client.verify_verification_code(
            data,
            authenticator=basic_authenticator,
        )
        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            content_type='application/json',
            data='{"code": "12345", "email": "test@example.com"}',
            method='POST',
            url='api/v1/verification-code/verify/',
            authenticator=basic_authenticator,
        )

    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_create_user_with_authenticator(self, mocked_request):
        self.client.create_user(
            email='test@testuser.com',
            password='mypassword',
            mobile_phone_number= "07111176523",
            authenticator=basic_authenticator,
        )

        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            content_type='application/json',
            data='{"email": "test@testuser.com", "password": "mypassword", "mobile_phone_number": "07111176523"}',
            method='POST',
            url='api/v1/user/',
            authenticator=basic_authenticator,
        )

    @mock.patch('directory_client_core.authentication.SessionSSOAuthenticator')
    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_get_user_questionnaire(self, mocked_request, mocked_authenticator):
        params = {'service': 'great'}
        self.client.get_user_questionnaire(sso_session_id=999, **params)
        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            method='GET',
            params=params,
            url='api/v1/user/questionnaire/',
            cache_control=None,
            authenticator=mocked_authenticator(),
        )

    @mock.patch('directory_client_core.authentication.SessionSSOAuthenticator')
    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_set_user_questionnaire_answer(self, mocked_request, mocked_authenticator):
        data = {'service': 'great', 'question_id': 1, 'answer': 'answer'}
        self.client.set_user_questionnaire_answer(sso_session_id=999, **data)
        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            content_type='application/json',
            method='POST',
            data=json.dumps(data),
            url='api/v1/user/questionnaire/',
            authenticator=mocked_authenticator(),
        )

    @mock.patch('directory_client_core.authentication.SessionSSOAuthenticator')
    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_get_user_data(self, mocked_request, mocked_authenticator):
        params = {'name': 'data_name'}
        self.client.get_user_data(sso_session_id=999, **params)
        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            method='GET',
            params=params,
            url='api/v1/user/data/',
            cache_control=None,
            authenticator=mocked_authenticator(),
        )

    @mock.patch('directory_client_core.authentication.SessionSSOAuthenticator')
    @mock.patch('directory_client_core.base.AbstractAPIClient.request')
    def test_set_user_data(self, mocked_request, mocked_authenticator):
        data = {'data': {'key': 'value'}, 'name': 'data_name'}
        self.client.set_user_data(sso_session_id=999, **data)
        assert mocked_request.call_count == 1
        assert mocked_request.call_args == mock.call(
            content_type='application/json',
            method='POST',
            data=json.dumps(data),
            url='api/v1/user/data/',
            authenticator=mocked_authenticator(),
        )
