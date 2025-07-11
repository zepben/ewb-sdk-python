#  Copyright $year Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["AuthProviderConfig"]

import warnings

import requests

from zepben.ewb.auth.common.auth_exception import AuthException
from zepben.ewb.auth.common.auth_method import AuthMethod


class ProviderDetails:
    token_endpoint: str
    jwk_uri: str

    def __init__(self, token_endpoint: str = "", jwk_uri: str = ""):
        self.token_endpoint = token_endpoint
        self.jwk_uri = jwk_uri


class AuthProviderConfig:
    auth_method: AuthMethod
    issuer: str
    audience: str
    provider_details: ProviderDetails

    def __init__(self, auth_method=AuthMethod.OAUTH, issuer: str = "", audience: str = "", provider_details: ProviderDetails = None):
        self.audience = audience
        self.issuer = issuer
        self.auth_method = auth_method
        self.provider_details = provider_details


def fetch_provider_details(issuer: str) -> ProviderDetails:
    try:
        issuer_url = f"{issuer.rstrip('/')}/.well-known/openid-configuration"
        response = requests.get(issuer_url)

    except Exception as e:
        warnings.warn(str(e))
        warnings.warn(f"Can't fetch provider details from {issuer_url}")
        raise ConnectionError(f"Can't fetch provider details from {issuer_url}")

    else:
        if response.ok:
            try:
                config_json = response.json()
                return ProviderDetails(jwk_uri=config_json.get("jwk_uri", ""), token_endpoint=config_json.get("token_endpoint", ""))
            except ValueError:
                raise AuthException(response.status_code, f"Expected JSON response from {issuer_url}, but got: {response.text}.")
        else:
            raise AuthException(
                response.status_code,
                f"{issuer_url} responded with: {response.reason} {response.text}"
            )


def create_auth_provider_config(conf_address: str, verify: bool, auth_type_field: str = "authType", issuer_field: str = "issuer",
                                audience_field: str = "audience") -> AuthProviderConfig:
    try:
        response = requests.get(conf_address, verify=verify)
    except Exception as e:
        warnings.warn(str(e))
        warnings.warn("If RemoteDisconnected, this process may hang indefinitely.")
        raise ConnectionError("Are you trying to connect to a HTTPS server with HTTP?")
    else:
        if response.ok:
            try:
                auth_config_json = response.json()
                auth_method = AuthMethod(auth_config_json[auth_type_field])
                if auth_method is not AuthMethod.NONE:
                    return AuthProviderConfig(
                        auth_method=auth_method,
                        issuer=auth_config_json[issuer_field],
                        audience=auth_config_json[audience_field],
                        provider_details=fetch_provider_details(auth_config_json[issuer_field])
                    )
                else:
                    raise AuthException(1, f"authMethod 'NONE' is not supported for token fetching!")

            except ValueError:
                raise AuthException(response.status_code, f"Expected JSON response from {conf_address}, but got: {response.text}.")
        else:
            raise AuthException(
                response.status_code,
                f"{conf_address} responded with: {response.reason} {response.text}"
            )
