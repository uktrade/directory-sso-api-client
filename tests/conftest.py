def pytest_configure():
    from django.conf import settings

    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'directory_sso_api_client',
        ],
        URLS_EXCLUDED_FROM_SIGNATURE_CHECK=[],
        DIRECTORY_SSO_API_CLIENT_BASE_URL='https://sso.com',
        DIRECTORY_SSO_API_CLIENT_API_KEY='test-api-key',
        DIRECTORY_SSO_API_CLIENT_SENDER_ID='test-sender',
        DIRECTORY_SSO_API_CLIENT_DEFAULT_TIMEOUT=5,
        AUTHENTICATION_BACKENDS=[
            'directory_sso_api_client.backends.SSOUserBackend',
        ],
        AUTH_USER_MODEL='directory_sso_api_client.SSOUser',
        MIDDLEWARE=[
            'django.contrib.sessions.middleware.SessionMiddleware',
            'directory_sso_api_client.middleware.AuthenticationMiddleware',
        ],
        SSO_SESSION_COOKIE='sso_session_cookie',
        SESSION_ENGINE='django.contrib.sessions.backends.signed_cookies',
        ROOT_URLCONF='tests.urls',
        SECRET_KEY='debug',
        ROOT_URL='http://greatcms.trade.bgs',
    )
