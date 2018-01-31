from directory_sso_api_client.base import BaseAPIClient


class DirectoryTestAPIClient(BaseAPIClient):

    endpoints = {
        'user_by_email': 'testapi/user-by-email/%s/'
    }

    def __init__(self, base_url=None, api_key=None):
        super(DirectoryTestAPIClient, self).__init__(base_url, api_key)

    def get_user_by_email(self, email, token):
        url = self.endpoints['user_by_email'] % email
        params = {"token": token}
        return self.get(url=url, params=params)
