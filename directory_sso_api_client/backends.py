import json
import logging

from requests.exceptions import RequestException

from django.conf import settings
from django.contrib import auth

from directory_sso_api_client import sso_api_client


logger = logging.getLogger(__name__)


class SSOUserBackend:
    MESSAGE_INVALID_JSON = (
        'SSO did not return JSON. A 502 may have occurred so SSO nginx '
        'redirected to http://sorry.great.gov.uk (see ED-2114)'
    )
    MESSAGE_NOT_SUCCESSFUL = 'SSO did not return a 200 response'

    def authenticate(self, request):
        session_id = request.COOKIES.get(settings.SSO_SESSION_COOKIE)
        if session_id:
            try:
                return self.get_user(session_id)
            except RequestException:
                logger.error(self.MESSAGE_NOT_SUCCESSFUL, exc_info=True)
            except json.JSONDecodeError:
                raise ValueError(self.MESSAGE_INVALID_JSON)

    def get_user(self, session_id):
        response = sso_api_client.user.get_session_user(session_id)
        response.raise_for_status()
        return self.build_user(session_id=session_id, parsed=response.json())

    def build_user(self, session_id, parsed):
        SSOUser = auth.get_user_model()
        return SSOUser(
            id=parsed['id'],
            session_id=session_id,
            hashed_uuid=parsed['hashed_uuid'],
            email=parsed['email'],
        )