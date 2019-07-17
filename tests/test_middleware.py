import requests_mock


def test_authenticcated(client, settings):
    client.cookies[settings.SSO_SESSION_COOKIE] = '123'

    with requests_mock.mock() as m:
        m.get(
            'https://sso.com/api/v1/session-user/',
            json={'id': 1, 'email': 'jim@example.com', 'hashed_uuid': 'thing'}
        )
        response = client.get('/')

    request = response.wsgi_request
    
    assert request.user.is_authenticated is True
    assert request.user.pk == 1
    assert request.user.email == 'jim@example.com'
    assert request.user.hashed_uuid == 'thing'


def test_not_authenticcated(client, settings):
    client.cookies[settings.SSO_SESSION_COOKIE] = '123'

    with requests_mock.mock() as m:
        m.get('https://sso.com/api/v1/session-user/', status_code=404)
        response = client.get('/')

    request = response.wsgi_request
    assert request.user.is_authenticated is False
