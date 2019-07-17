# Changelog

## [5.1.1](https://pypi.org/project/directory-sso-api-client/5.1.1/) (2019-07-16)
[Full Changelog](https://github.com/uktrade/directory-sso-api-client/pull/38/files)

### Bugs fixed

- Allow user model to be pluggable


## [5.1.0](https://pypi.org/project/directory-sso-api-client/5.1.0/) (2019-07-14)
[Full Changelog](https://github.com/uktrade/directory-sso-api-client/pull/37/files)

### Implemented enhancements

- Added authentication backend

## [5.0.1](https://pypi.org/project/directory-sso-api-client/5.0.1/) (2019-07-04)
[Full Changelog](https://github.com/uktrade/directory-sso-api-client/pull/36/files)

### Implemented enhancements
- No ticket - Can now import the instantiated client as `from directory_sso_api_client import sso_api_client`
- No ticket - Remove `version.py`

### Bugs fixed
- No ticket - Upgrade vulnerable django version to django 1.11.22


## [5.0.0](https://pypi.org/project/directory-sso-api-client/5.0.0/) (2019-04-23)
[Full Changelog](https://github.com/uktrade/directory-sso-api-client/pull/35/files)

### Implemented enhancements

- Upgraded directory client core to reduce overzealous logging from the fallback cache.
- Improved documentation in readme.
- The client responses are now subclasses of `request.Response`.
- README.md now renders nicely in PyPi.
- Improve packaging by moving development requirements to setup.py

### Breaking changes

- Directory client core has been upgraded a major version 5.0.0. [See](https://github.com/uktrade/directory-client-core/pull/16)
- Dropped support for Python 3.5
- The client responses dropped the `raw_response` property. The attributes of `raw_response` are now available on the client responses.