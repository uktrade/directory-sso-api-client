from directory_sso_api_client.base import BaseAPIClient


class DirectoryTestAPIClient(BaseAPIClient):

    endpoints = {
        'user_by_email': 'testapi/user-by-email/{email}/'
    }

    def get_user_by_email(self, email: str):
        result = None
        if email:
            url = self.endpoints['user_by_email'].format(email=email)
            result = self.get(url=url)
        return result
