from unittest import mock

import pytest
import requests
import requests_mock

from django.contrib.auth import authenticate

from directory_sso_api_client import backends, sso_api_client


@pytest.fixture
def sso_request(rf, settings, client):
    request = rf.get('/')
    request.COOKIES[settings.SSO_SESSION_COOKIE] = '123'
    request.session = client.session
    return request


@mock.patch.object(sso_api_client.user, 'get_session_user')
def test_remote_sso_backend_no_cookie(mock_get_session_user, rf):
    request = rf.get('/')

    assert authenticate(request) is None
    assert mock_get_session_user.call_count == 0


@mock.patch.object(
    sso_api_client.user, 'get_session_user',
    wraps=sso_api_client.user.get_session_user
)
def test_remote_sso_backend_api_response_ok(
    mock_get_session_user, sso_request
):
    with requests_mock.mock() as m:
        m.get(
            'https://sso.com/api/v1/session-user/',
            json={'id': 1, 'email': 'jim@example.com', 'hashed_uuid': 'thing'}
        )
        user = authenticate(sso_request)
        assert user.pk == 1
        assert user.id == 1
        assert user.email == 'jim@example.com'
        assert user.hashed_uuid == 'thing'

    assert mock_get_session_user.call_count == 1
    assert mock_get_session_user.call_args == mock.call('123')


def test_remote_sso_backend_bad_response(sso_request):
    with requests_mock.mock() as m:
        m.get(
            'https://sso.com/api/v1/session-user/',
            status_code=400,
        )
        assert authenticate(sso_request) is None


def test_remote_sso_backend_not_josn_response(sso_request):
    with requests_mock.mock() as m:
        m.get(
            'https://sso.com/api/v1/session-user/',
            text='<html></html>'
        )
        with pytest.raises(ValueError):
            assert authenticate(sso_request) is None


@pytest.mark.parametrize(
    'excpetion_class', requests.exceptions.RequestException.__subclasses__()
)
def test_remote_sso_backend_timeout(sso_request, caplog, excpetion_class):
    with requests_mock.mock() as m:
        m.get(
            'https://sso.com/api/v1/session-user/',
            exc=excpetion_class
        )
        assert authenticate(sso_request) is None

    log = caplog.records[0]
    assert log.levelname == 'ERROR'
    assert log.msg == backends.SSOUserBackend.MESSAGE_NOT_SUCCESSFUL
