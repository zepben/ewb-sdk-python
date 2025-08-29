![Build Status](https://img.shields.io/github/actions/workflow/status/zepben/evolve-sdk-python/python-lib-snapshot.yml)
[![codecov](https://codecov.io/gh/zepben/evolve-sdk-python/branch/main/graph/badge.svg?token=B0WNRMMR77)](https://codecov.io/gh/zepben/evolve-sdk-python)

# Zepben Evolve Python SDK #
The Python Evolve SDK contains everything necessary to communicate with a [Zepben EWB Server](https://github.com/zepben/energy-workbench-server). See the complete [Evolve Python SDK Documentation](https://zepben.github.io/evolve/docs/python-sdk/) for more details.

# Requirements #

- Python 3.10 or later

# Installation #

```
pip install zepben.ewb
```

# Building #

```
python setup.py bdist_wheel
```
    
# Usage #

See [Evolve Python SDK Documentation](https://zepben.github.io/evolve/docs/python-sdk/).

# Zepben Auth Library #

This library provides Authentication mechanisms for Zepben SDKs used with Energy Workbench and other Zepben services.

Typically, this library will be used by the SDKs to plug into connection mechanisms. It is unlikely that end users will
need to use this library directly.

# Example Usage #

```python
from zepben.ewb.client import get_token_fetcher

authenticator = get_token_fetcher(
    issuer="https://login.microsoftonline.com/293784982371c-8797-4168-a5e7-923874928734/v2.0/",
    audience="49875987458e-e217-4c8f-abf6-394875984758",
    client_id="asdaf98798-0584-41c3-b30c-1f9874596da",
    username="",
    password=""
)

authenticator.token_request_data.update({
    'grant_type': 'client_credentials',
    'client_secret': 'W.Tt5KSzX6Q28lksdajflkajsdflkjaslkdjfxx',
    'client_id': 'asdaf98798-0584-41c3-b30c-1f9874596da',
    'scope': '9873498234-e217-4c8f-abf6-9789889987/.default'})
#

print(authenticator.fetch_token())
```
