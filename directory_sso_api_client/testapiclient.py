from directory_sso_api_client.base import BaseAPIClient


class DirectoryTestAPIClient(BaseAPIClient):

    endpoints = {
        'user_by_email': 'testapi/user-by-email/{email}/'
    }

    def __init__(self, base_url=None, api_key=None):
        super(DirectoryTestAPIClient, self).__init__(base_url, api_key)

    def get_user_by_email(self, email: str, token: str):
        result = None
        if email and token:
            url = self.endpoints['user_by_email'].format(email=email)
            params = {"token": token}
            result = self.get(url=url, params=params)
        return result
