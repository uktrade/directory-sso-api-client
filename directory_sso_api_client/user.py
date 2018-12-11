from collections import OrderedDict

from directory_client_core.base import AbstractAPIClient
from directory_client_core.authentication import BearerAuthenticator

from directory_sso_api_client.version import __version__


class UserAPIClient(AbstractAPIClient):

    endpoints = {
        'session_user': 'api/v1/session-user/',
        'oauth2_user_profile': 'oauth2/user-profile/v1/',
        'last_login': 'api/v1/last-login/',
        'check_password': 'api/v1/password-check/'
    }
    version = __version__

    def get_session_user(self, session_id, cookies=None):
        return self.get(
            url=self.endpoints['session_user'],
            params={'session_key': session_id},
            cookies=cookies,
        )

    def get_oauth2_user_profile(self, bearer_token, cookies=None):
        return self.get(
            url=self.endpoints['oauth2_user_profile'],
            authenticator=BearerAuthenticator(bearer_token),
            cookies=cookies,
        )

    def check_password(self, session_id, password, cookies=None):
        url = self.endpoints['check_password']
        data = OrderedDict(
            [('session_key', session_id), ('password', password)]
        )
        return self.post(url, data, cookies=cookies)

    def get_last_login(self, start=None, end=None, cookies=None):
        params = {}
        if start is not None:
            params['start'] = start
        if end is not None:
            params['end'] = end
        params = params or None

        return self.get(
            url=self.endpoints['last_login'],
            params=params,
            cookies=cookies,
        )
