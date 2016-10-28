# directory-sso-api-client
[Export Directory SSO API client](https://www.directory.exportingisgreat.gov.uk/)

## Build status

[![CircleCI](https://circleci.com/gh/uktrade/directory-sso-api-client/tree/master.svg?style=svg)](https://circleci.com/gh/uktrade/directory-sso-api-client/tree/master)

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
