from directory_sso_api_client.base import BaseAPIClient


class UserAPIClient(BaseAPIClient):

    endpoints = {
        'session_user': 'session-user/',
        'last_login': 'last-login/',
    }

    def get_session_user(self, session_id):
        return self.get(
            url=self.endpoints['session_user'],
            params={'session_key': session_id}
        )

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
