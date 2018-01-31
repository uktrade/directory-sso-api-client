from directory_sso_api_client.base import BaseAPIClient
from directory_sso_api_client.user import UserAPIClient


class DirectoryTestAPIClient(BaseAPIClient):

    endpoints = {
        'user_by_email': 'testapi/user-by-email/%s/'
    }

    def __init__(self, base_url=None, api_key=None):
        super(DirectoryTestAPIClient, self).__init__(base_url, api_key)
        self.user = UserAPIClient(base_url, api_key)

    def get_user_by_email(self, email):
        url = self.endpoints['user_by_email'] % email
        return self.get(url=url)
