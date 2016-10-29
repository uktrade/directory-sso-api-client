from directory_sso_api_client.base import BaseAPIClient


class UserAPIClient(BaseAPIClient):

    endpoints = {
        'session_user': 'session-user/'
    }

    def get_session_user(self, session_id):
        return self.get(
            url=self.endpoints['session_user'],
            params={'session_key': session_id}
        )
