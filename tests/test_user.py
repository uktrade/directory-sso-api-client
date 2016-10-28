from unittest import TestCase

from tests import stub_request

from directory_sso_api_client.user import UserAPIClient


class UserAPIClientTest(TestCase):

    def setUp(self):
        self.client = UserAPIClient(
            base_url='https://example.com', api_key='test'
        )

    @stub_request('https://example.com/session-user/', 'get')
    def test_get_session_user(self, stub):
        self.client.get_session_user(session_id=1)
