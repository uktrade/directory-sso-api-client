# directory-sso-api-client

[![code-climate-image]][code-climate]
[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![pypi-image]][pypi]
[![semver-image]][semver]

**[Directory SSO API client](https://great.gov.uk/)**

---

## Installation

```sh
    $ pip install directory-sso-api-client
```

The api client expects the following settings:

| Setting                                  | Notes                                                       |
| ---------------------------------------- | ----------------------------------------------------------- |
| DIRECTORY_SSO_API_CLIENT_BASE_URL        |                                                             |
| DIRECTORY_SSO_API_CLIENT_API_KEY         | Unique to client. Retrieved during the on-boarding process. |
| DIRECTORY_SSO_API_CLIENT_SENDER_ID       | Unique to client. Retrieved during the on-boarding process. |
| DIRECTORY_SSO_API_CLIENT_DEFAULT_TIMEOUT |                                                             |

Once that is done the API client can be used:

```py
from directory_sso_api_client.client import sso_api_client
```

## Authentication backend

Add the following to your settings

```
AUTHENTICATION_BACKENDS = ['directory_sso_api_client.backends.SSOUserBackend']

AUTH_USER_MODEL='directory_sso_api_client.SSOUser',

MIDDLEWARE_CLASSES = [
    ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    ...
```

That will result in the user being authenticate via their sso session cookie and then attached to `request.user`.

## Development

```shell
$ git clone https://github.com/uktrade/directory-sso-api-client
$ cd directory-sso-api-client
$ [create virtual environment and activate]
$ pip install -r requirements_test.txt
```

## Publish to PyPI

The package should be published to PyPI on merge to master. If you need to do it locally then get the credentials from rattic and add the environment variables to your host machine:

| Setting                     |
| --------------------------- |
| DIRECTORY_PYPI_USERNAME     |
| DIRECTORY_PYPI_PASSWORD     |

Then run the following command:
```sh
    make publish
```


[code-climate-image]: https://codeclimate.com/github/uktrade/directory-sso-api-client/badges/issue_count.svg
[code-climate]: https://codeclimate.com/github/uktrade/directory-sso-api-client

[circle-ci-image]: https://circleci.com/gh/uktrade/directory-sso-api-client/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/directory-sso-api-client/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/directory-sso-api-client/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/directory-sso-api-client

[pypi-image]: https://badge.fury.io/py/directory-sso-api-client.svg
[pypi]: https://badge.fury.io/py/directory-sso-api-client

[semver-image]: https://img.shields.io/badge/Versioning%20strategy-SemVer-5FBB1C.svg
[semver]: https://semver.org
