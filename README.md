# directory-sso-api-client

[![code-climate-image]][code-climate]
[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![gemnasium-image]][gemnasium]

**[Export Directory SSO API client](https://www.directory.exportingisgreat.gov.uk/)**

---

## Requirements

## Installation

```shell
pip install -e git+https://git@github.com/alphagov/directory-sso-api-client.git@0.0.1#egg=directory-sso-api-client
```

## Usage

```python
from directory_sso_api_client.client import DirectorySSOAPIClient

directory_sso_client = DirectorySSOAPIClient(
    base_url="https://account.trade.great.gov.uk/api",
    api_key=api_key
)
```

### Get user by session ID

```python
directory_sso_client.user.get(
    session_id=session_id
)
```

## Development

    $ git clone https://github.com/uktrade/directory-sso-api-client
    $ cd directory-ui
    $ make


[code-climate-image]: https://codeclimate.com/github/uktrade/directory-sso-api-client/badges/issue_count.svg
[code-climate]: https://codeclimate.com/github/uktrade/directory-sso-api-client

[circle-ci-image]: https://circleci.com/gh/uktrade/directory-sso-api-client/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/directory-sso-api-client/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/directory-sso-api-client/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/directory-sso-api-client

[gemnasium-image]: https://gemnasium.com/badges/github.com/uktrade/directory-sso-api-client.svg
[gemnasium]: https://gemnasium.com/github.com/uktrade/directory-sso-api-client
