from collections import OrderedDict
import pkg_resources

from directory_client_core.base import AbstractAPIClient
from directory_client_core.authentication import AuthenticatorNegotiator


class UserAPIClient(AbstractAPIClient):

    endpoints = {
        'session_user': 'api/v1/session-user/',
        'oauth2_user_profile': 'oauth2/user-profile/v1/',
        'last_login': 'api/v1/last-login/',
        'check_password': 'api/v1/password-check/',
        'regenerate_verification': 'api/v1/verification-code/regenerate/',
        'verify_verification': 'api/v1/verification-code/verify/',
        'user_create': 'api/v1/user/',
        'user_create_profile': 'api/v1/user/profile/',
        'user_update_profile': 'api/v1/user/profile/update/',
    }
    version = pkg_resources.get_distribution(__package__).version

    def get_session_user(self, session_id, authenticator=None):
        return self.get(
            url=self.endpoints['session_user'],
            params={'session_key': session_id},
            authenticator=authenticator,
        )

    def get_oauth2_user_profile(self, bearer_token):
        return self.get(
            url=self.endpoints['oauth2_user_profile'],
            authenticator=AuthenticatorNegotiator(bearer_token=bearer_token)
        )

    def regenerate_verification_code(self, data, authenticator=None):
        return self.post(
            url=self.endpoints['regenerate_verification'],
            data=data,
            authenticator=authenticator,
        )

    def verify_verification_code(self, data, authenticator=None):
        return self.post(
            url=self.endpoints['verify_verification'],
            data=data,
            authenticator=authenticator,
        )

    def check_password(self, session_id, password, authenticator=None):
        url = self.endpoints['check_password']
        data = OrderedDict(
            [('session_key', session_id), ('password', password)]
        )
        return self.post(
            url,
            data,
            authenticator=authenticator,
        )

    def get_last_login(self, start=None, end=None, authenticator=None):
        params = {}
        if start is not None:
            params['start'] = start
        if end is not None:
            params['end'] = end
        params = params or None

        return self.get(
            url=self.endpoints['last_login'],
            params=params,
            authenticator=authenticator,
        )

    def create_user(self, email, password, authenticator=None):
        url = self.endpoints['user_create']
        data = OrderedDict(
            [('email', email), ('password', password)]
        )
        return self.post(
            url,
            data,
            authenticator=authenticator,
        )

    def create_user_profile(self, sso_session_id, data):
        authenticator = AuthenticatorNegotiator(sso_session_id=sso_session_id)
        url = self.endpoints['user_create_profile']
        return self.post(url, data, authenticator=authenticator)

    def update_user_profile(self, sso_session_id, data):
        authenticator = AuthenticatorNegotiator(sso_session_id=sso_session_id)
        url = self.endpoints['user_update_profile']
        return self.patch(url, data, authenticator=authenticator)
