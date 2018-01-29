from urllib.parse import urljoin

from collections import OrderedDict

from directory_sso_api_client.base import BaseAPIClient


class UserAPIClient(BaseAPIClient):

    endpoints = {
        'session_user': 'api/v1/session-user/',
        'oauth2_user_profile': 'oauth2/user-profile/v1/',
        'last_login': 'api/v1/last-login/',
        'check_password': 'api/v1/password-check/',
        'user_by_email': 'api/v1/user-by-email/'
    }

    def get_session_user(self, session_id):
        return self.get(
            url=self.endpoints['session_user'],
            params={'session_key': session_id}
        )

    def get_oauth2_user_profile(self, bearer_token):
        headers = {'Authorization': 'Bearer {}'.format(bearer_token)}
        return self.get(
            url=self.endpoints['oauth2_user_profile'],
            headers=headers
        )

    def check_password(self, session_id, password):
        url = self.endpoints['check_password']
        data = OrderedDict(
            [('session_key', session_id), ('password', password)]
        )
        return self.post(url, data)

    def get_last_login(self, start=None, end=None):
        params = {}
        if start is not None:
            params['start'] = start
        if end is not None:
            params['end'] = end
        params = params or None

        return self.get(
            url=self.endpoints['last_login'],
            params=params
        )

    def get_user_by_email(self, email):
        return self.get(
            url=urljoin(self.endpoints['user_by_email'], email + "/")
        )
