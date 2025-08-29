#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["ZepbenTokenFetcher", "create_token_fetcher", "get_token_fetcher", "create_token_fetcher_managed_identity"]

import warnings
from dataclasses import dataclass, Field, field, InitVar
from datetime import datetime
from typing import Optional, Callable

import jwt
import requests
from requests import Response
from urllib3.exceptions import InsecureRequestWarning

from zepben.ewb.auth.common.auth_exception import AuthException
from zepben.ewb.auth.common.auth_method import AuthMethod
# noinspection PyProtectedMember
from zepben.ewb.auth.common.auth_provider_config import AuthProviderConfig, create_auth_provider_config, fetch_provider_details


def _fetch_token_generator(
    is_entraid: bool,
    use_identity: bool,
    identity_url: Optional[str] = None
) -> Callable[[dict, dict, str, Optional[bool], Optional[bool]], Response]:

    def post(
        refresh_request_data: dict,
        token_request_data: dict,
        token_endpoint: str,
        refresh: bool,
        verify: bool
    ):

        # EntraID requires a scope of the audience + /.default. We strip the / just in case so we don't end up with 2 slashes.
        if is_entraid:
            refresh_request_data["scope"] = refresh_request_data["audience"] + "/.default"
            # Also requires grant type client credentials for access tokens
            token_request_data.update({
                'grant_type': 'client_credentials',
                'scope': refresh_request_data["audience"] + "/.default"

            })

        return requests.post(
            url=token_endpoint,
            headers={"content-type": "application/x-www-form-urlencoded"},
            data=refresh_request_data if refresh else token_request_data,
            verify=verify
        )

    def _get_token_response(
        refresh_request_data: dict,
        token_request_data: dict,
        token_endpoint: str,
        refresh: bool,
        verify: bool
    ) -> requests.Response:

        refresh = not is_entraid and refresh  # At the moment Azure auth doesn't support refresh tokens. So we always force new tokens.

        return post(
            refresh_request_data,
            token_request_data,
            token_endpoint,
            refresh,
            verify
        )

    def _get_token_response_from_identity(
        refresh_request_data: dict,
        token_request_data: dict,
        token_endpoint: str,
        refresh: Optional[bool] = False,
        verify: Optional[bool] = False
    ) -> requests.Response:

        return requests.get(identity_url, headers={"Metadata": "true"}, verify=verify)

    if use_identity:
        if not identity_url:
            raise ValueError("Misconfiguration detected - if use_identity is true, identity_url must also be provided. This is a bug, contact Zepben.")
        return _get_token_response_from_identity
    else:
        return _get_token_response


@dataclass(init=True, repr=True, eq=True)
class ZepbenTokenFetcher:
    """
    Fetches access tokens from an authentication provider using the OAuth 2.0 protocol.

    :param audience: Audience to use when requesting tokens
    :param token_endpoint: The domain of the token issuer.
    :param token_request_data: Data to pass in token requests.
    :param refresh_request_data: Data to pass in refresh token requests.
    :param verify: Passed through to requests.post(). When this is a boolean, it determines whether to verify the HTTPS
        certificate of the OAUTH service or not. When this is a string, it is used as the filename of the certificate
        truststore to use when verifying the OAUTH service.
    :param auth_method:  Deprecated. Kept for backwards compatibility, but this is now unused.
    """

    audience: str
    issuer: Optional[str] = None
    token_endpoint: Optional[str] = None
    token_request_data: Optional[dict] = field(default_factory=dict)
    refresh_request_data: Optional[dict] = field(default_factory=dict)
    verify: Optional[bool | str] = None
    auth_method: Optional[AuthMethod] = None

    _request_token: InitVar[Callable[[dict, dict, str, Optional[bool], Optional[bool]], requests.Response]] = None

    _access_token: Optional[str] = None
    _refresh_token: Optional[str] = None
    _token_expiry: Optional[datetime] = datetime.min
    token_type: Optional[str] = None

    def __post_init__(self, _request_token):
        if _request_token is None:
            _request_token = _fetch_token_generator(False, False)
        self._request_token = _request_token

        self.token_request_data["audience"] = self.audience
        self.refresh_request_data["audience"] = self.audience

    def fetch_token(self) -> str:
        """
        Returns a JWT access token and its type in the form of '<type> <3 part JWT>', retrieved from the configured OAuth2 token provider.
        Throws AuthException if an access token request fails.
        """
        if datetime.utcnow() > self._token_expiry:
            # Stored token has expired, try to refresh
            self._access_token = None
            if self._refresh_token:
                self._fetch_token(refresh=True)

            if self._access_token is None:
                # If using the refresh token did not work for any reason, self._access_token will still be None.
                # and thus we must try get a fresh access token using credentials instead.
                self._fetch_token()

            # Just to give a friendly error if a token retrieval failed for a case we haven't handled.
            if not self._token_type or not self._access_token:
                raise Exception(
                    f"Token couldn't be retrieved from {self.token_endpoint} using configuration "
                    f"{self.auth_method}, audience: {self.audience}"
                )

        return f"{self._token_type} {self._access_token}"

    def _fetch_token(self, refresh: Optional[bool] = False):
        if refresh:
            self.refresh_request_data["refresh_token"] = self._refresh_token

        # We currently only support EntraID and Auth0
        # TODO: convert this into a callback passed into __init__ that fetches the token.

        response: requests.Response
        response = self._request_token(
            self.refresh_request_data,
            self.token_request_data,
            self.token_endpoint,
            refresh,
            self.verify
        )

        if not response.ok:
            raise AuthException(response.status_code, f'Token fetch failed, Error was: {response.reason} {response.text}')

        try:
            data = response.json()
        except ValueError:
            raise AuthException(response.status_code, f'Response did not contain expected JSON - response was: {response.text}')

        if "error" in data or "access_token" not in data:
            raise AuthException(
                response.status_code,
                f'{data.get("error", "Access Token absent in token response")} - {data.get("error_description", f"Response was: {data}")}'
            )

        self._token_type = data["token_type"]
        self._access_token = data["access_token"]
        self._token_expiry = datetime.fromtimestamp(jwt.decode(self._access_token, options={"verify_signature": False})['exp'])

        if refresh:
            self._refresh_token = data.get("refresh_token", None)


def create_token_fetcher(
    conf_address: str,
    verify_conf: Optional[bool | str] = True,
    verify_auth: Optional[bool | str] = True,
    auth_type_field: Optional[str] = "authType",
    audience_field: Optional[str] = "audience",
    issuer_field: Optional[str] = "issuer",
) -> Optional[ZepbenTokenFetcher]:
    """
    Helper method to fetch auth related configuration from `conf_address` and create a :class:`ZepbenTokenFetcher`

    :param conf_address: The url to retrieve the authentication config from.
    :param verify_conf: Passed through to requests.get() when retrieving the authentication config. When this is a boolean, it determines whether to verify
                        the HTTPS certificate of `conf_address`. When this is a string, it is used as the filename of the certificate truststore to use
                        when verifying `conf_address`.
    :param verify_auth: Passed through to the resulting :class:`ZepbenTokenFetcher`.
    :param auth_type_field: The field name to look up in the JSON response from the conf_address for `auth_type`.
    :param audience_field: The field name to look up in the JSON response from the conf_address for `audience`.
    :param issuer_field: The field name to look up in the JSON response from the conf_address for `issuer`.

    :returns: A :class:`ZepbenTokenFetcher` if the server reported authentication was configured, otherwise None.
    """

    with warnings.catch_warnings():
        if not verify_conf:
            warnings.filterwarnings("ignore", category=InsecureRequestWarning)

        config = create_auth_provider_config(
            conf_address,
            verify_conf,
            auth_type_field=auth_type_field,
            issuer_field=issuer_field,
            audience_field=audience_field)

        if config.auth_method is not AuthMethod.NONE:
            return ZepbenTokenFetcher(
                auth_method=config.auth_method,
                audience=config.audience,
                token_endpoint=config.provider_details.token_endpoint,
                verify=verify_auth,
                _request_token=_fetch_token_generator(config.auth_method is AuthMethod.ENTRAID, False)
            )

    return None


def get_token_fetcher(audience: str, issuer: str, client_id: str, username: str, password: str) -> ZepbenTokenFetcher:
    """
    Create a token fetcher for the given audience and client, using username and password.

    :param audience: The OAuth audience for this client.
    :param issuer: The domain of the issuer - e.g zepben.au.auth0.com
    :param client_id: The client id to use.
    :param username: The user to log in as. Must have access to the provided audience.
    :param password: The corresponding password for the user.
    """

    config = AuthProviderConfig(
        issuer=issuer,
        audience=audience,
        provider_details=fetch_provider_details(issuer)
    )

    token_fetcher = ZepbenTokenFetcher(audience=audience, token_endpoint=config.provider_details.token_endpoint, auth_method=AuthMethod.OAUTH)
    token_fetcher.token_request_data.update({
        'client_id': client_id,
        'scope': 'offline_access openid profile email0'
    })
    token_fetcher.refresh_request_data.update({
        "grant_type": "refresh_token",
        'client_id': client_id,
        'scope': 'offline_access openid profile email0'
    })
    token_fetcher.token_request_data.update({
        'grant_type': 'password',
        'username': username,
        'password': password
    })

    return token_fetcher


def create_token_fetcher_managed_identity(identity_url: str, verify_auth: bool) -> ZepbenTokenFetcher:
    """
    Create a token fetcher specifically for use with Azure Managed Identities.
    Most fields of the token fetcher will be unused, as they exist only for fetching tokens from token endpoints.
    _request_token is overridden to use a simplified function which simply given an URL to fetch tokens from will return
    a token for a host with a valid managed identity.
    
    :param identity_url: The URL to fetch a token from. Should contain the resource ID. Typically looks like:
    "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=5ffcfee6-34cd-4c5c-bb7e-c5261d739341"
    :param verify_auth: Whether to verify certificates for the identity_url. Only applies for https URLs.
    """

    return ZepbenTokenFetcher(
        audience="",
        issuer="",
        token_endpoint="",
        verify=verify_auth,
        _request_token=_fetch_token_generator(True, True, identity_url)
    )
