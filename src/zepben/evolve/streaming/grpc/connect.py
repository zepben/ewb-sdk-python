#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional, Union

import grpc
from zepben.auth import ZepbenTokenFetcher, create_token_fetcher, create_token_fetcher_managed_identity
from zepben.evolve import GrpcChannelBuilder

__all__ = ["connect_tls", "connect_insecure", "connect_with_password", "connect_with_secret", "connect_with_identity", "connect_with_token"]

GRPC_READY_TIMEOUT = 20  # seconds


def connect_insecure(
    host: str = "localhost",
    rpc_port: int = 50051,
    **kwargs
) -> grpc.aio.Channel:
    """
    Create a :class:`grpc.aio.Channel` that communicates with the gRPC service over plaintext.

    :param host: The hostname where the gRPC service is hosted
    :param rpc_port: The port of the gRPC service
    :return: A plaintext connection to the gRPC service
    """
    return GrpcChannelBuilder().for_address(host, rpc_port).build(**kwargs)


def connect_tls(
    host: str = "localhost",
    rpc_port: int = 50051,
    ca_filename: Optional[str] = None,
    **kwargs
) -> grpc.aio.Channel:
    """
    Create a :class:`grpc.aio.Channel` that communicates with the gRPC service using SSL/TLS transport security.

    :param host: The hostname where the gRPC service is hosted
    :param rpc_port: The port of the gRPC service
    :param ca_filename: The filename of a truststore containing additional trusted root certificates. This parameter is optional
                        and defaults to null, in which case only the system CAs are used to verify certificates.
    :return:An encrypted connection to the gRPC service
    """
    return GrpcChannelBuilder().for_address(host, rpc_port).make_secure(root_certificates=ca_filename).build(**kwargs)


def connect_with_identity(host: str,
                          rpc_port: int,
                          identity_url: str,
                          ca_filename: Optional[str] = None,
                          verify_auth: bool = True,
                          **kwargs) -> grpc.aio.Channel:
    """
    Create a :class:`grpc.aio.Channel` that communicates with the gRPC service using SSL/TLS transport security and the OAuth client credentials flow,
    utilising an Azure managed identity for fetching access tokens.

    :param host: The hostname where the gRPC service is hosted
    :param rpc_port: The port of the gRPC service
    :param identity_url: The URL including resource identifier (API) to fetch token from. Typically something like:
                         http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=<SOME_IDENTIFIER>
    :param ca_filename: The filename of a truststore containing additional trusted root certificates. This parameter is optional
                        and defaults to null, in which case only the system CAs are used to verify certificates.
    :param verify_auth: Passed through to `requests.post()` when fetching access tokens to verify certificates of the auth service.
    :return: An authenticated, encrypted connection to the gRPC service based on OAuth2 flows. If the authentication configuration specifies that no
             authentication is required, a non-authenticated, encrypted connection is returned instead.
    """
    token_fetcher = create_token_fetcher_managed_identity(identity_url, verify_auth)
    return GrpcChannelBuilder().for_address(host, rpc_port).make_secure(root_certificates=ca_filename).with_token_fetcher(token_fetcher).build(**kwargs)


def connect_with_secret(
    client_id: str,
    client_secret: str,
    host: str = "localhost",
    rpc_port: int = 50051,
    conf_address: Optional[str] = None,
    verify_conf: Union[bool, str] = True,
    verify_auth: Union[bool, str] = True,
    ca_filename: Optional[str] = None,
    **kwargs
) -> grpc.aio.Channel:
    """
    Create a :class:`grpc.aio.Channel` that communicates with the gRPC service using SSL/TLS transport security and the OAuth client credentials flow.
    The OAuth provider's domain and the "audience" parameter of the token request are fetched as JSON from a specified URL.

    :param client_id: The client ID of the OAuth application to authenticate for
    :param client_secret: The client secret of the OAuth application to authenticate for
    :param host: The hostname where the gRPC service is hosted
    :param rpc_port: The port of the gRPC service
    :param conf_address: The address of the authentication configuration
    :param verify_conf: Passed through to `requests.get()` when fetching the authentication configuration
    :param verify_auth: Passed through to `requests.post()` when fetching access tokens to verify certificates of the auth service.
    :param ca_filename: The filename of a truststore containing additional trusted root certificates. This parameter is optional
                        and defaults to null, in which case only the system CAs are used to verify certificates.
    :return: An authenticated, encrypted connection to the gRPC service based on OAuth2 flows. If the authentication configuration specifies that no
             authentication is required, a non-authenticated, encrypted connection is returned instead.
    """
    token_fetcher = create_token_fetcher(
        conf_address=conf_address or f"https://{host}/ewb/auth",
        verify_conf=verify_conf,
        verify_auth=verify_auth
    )

    if token_fetcher:
        return _connect_with_secret_using_token_fetcher(token_fetcher, client_id, client_secret, host, rpc_port, ca_filename, **kwargs)
    else:
        return connect_tls(host, rpc_port, ca_filename, **kwargs)


def connect_with_token(
    access_token: str,
    host: str = "localhost",
    rpc_port: int = 50051,
    ca_filename: Optional[str] = None,
    **kwargs
) -> grpc.aio.Channel:
    """
    Create a :class:`grpc.aio.Channel` that communicates with the gRPC service using SSL/TLS transport security and a personal access token generated from Evolve App Server or Evolve Web Client.

    :param access_token: The token string of the client generated using Evolve App
    :param host: The hostname where the gRPC service is hosted
    :param rpc_port: The port of the gRPC service
    :param ca_filename: The filename of a truststore containing additional trusted root certificates. This parameter is optional
                        and defaults to null, in which case only the system CAs are used to verify certificates.
    :return: An authenticated, encrypted connection to the gRPC service based on OAuth2 flows. If the authentication configuration specifies that no
             authentication is required, a non-authenticated, encrypted connection is returned instead.
    """

    return GrpcChannelBuilder().for_address(host, rpc_port).make_secure(root_certificates=ca_filename).with_client_token(access_token).build(**kwargs)


def connect_with_password(
    client_id: str,
    username: str,
    password: str,
    host: str = "localhost",
    rpc_port: int = 50051,
    conf_address: Optional[str] = None,
    verify_conf: Union[bool, str] = True,
    verify_auth: Union[bool, str] = True,
    ca_filename: Optional[str] = None,
    **kwargs
) -> grpc.aio.Channel:
    """
    Create a :class:`grpc.aio.Channel` that communicates with the gRPC service using SSL/TLS transport security and the OAuth password grant flow.
    The OAuth provider's domain and the "audience" parameter of the token request are fetched as JSON from a specified URL.

    :param client_id: The client ID of the OAuth application to authenticate for
    :param username: The username of the user to authenticate with
    :param password: The password of the user to authenticate with
    :param host: The hostname where the gRPC service is hosted
    :param rpc_port: The port of the gRPC service
    :param conf_address: The address of the authentication configuration
    :param verify_conf: Passed through to `requests.get()` when fetching the authentication configuration
    :param verify_auth: Passed through to `requests.post()` when fetching access tokens to verify certificates of the auth service.
    :param ca_filename: The filename of a truststore containing additional trusted root certificates. This parameter is optional
                        and defaults to null, in which case only the system CAs are used to verify certificates.
    :return: An authenticated, encrypted connection to the gRPC service based on OAuth2 flows. If the authentication configuration specifies that no
             authentication is required, a non-authenticated, encrypted connection is returned instead.
    """
    token_fetcher = create_token_fetcher(
        conf_address=conf_address or f"https://{host}/ewb/auth",
        verify_conf=verify_conf,
        verify_auth=verify_auth
    )

    if token_fetcher:
        return _connect_with_password_using_token_fetcher(token_fetcher, client_id, username, password, host, rpc_port, ca_filename, **kwargs)
    else:
        return connect_tls(host, rpc_port, ca_filename, **kwargs)


def _connect_with_secret_using_token_fetcher(
    token_fetcher: ZepbenTokenFetcher,
    client_id: str,
    client_secret: str,
    host: str,
    rpc_port: int,
    ca_filename: Optional[str],
    **kwargs
) -> grpc.aio.Channel:
    token_fetcher.token_request_data["client_id"] = client_id
    token_fetcher.token_request_data["client_secret"] = client_secret
    token_fetcher.token_request_data["grant_type"] = "client_credentials"

    return GrpcChannelBuilder().for_address(host, rpc_port).make_secure(root_certificates=ca_filename).with_token_fetcher(token_fetcher).build(**kwargs)


def _connect_with_password_using_token_fetcher(
    token_fetcher: ZepbenTokenFetcher,
    client_id: str,
    username: str,
    password: str,
    host: str,
    rpc_port: int,
    ca_filename: Optional[str],
    **kwargs
) -> grpc.aio.Channel:
    token_fetcher.token_request_data["client_id"] = client_id
    token_fetcher.token_request_data["username"] = username
    token_fetcher.token_request_data["password"] = password
    token_fetcher.token_request_data["grant_type"] = "password"
    token_fetcher.token_request_data["scope"] = "offline_access"

    return GrpcChannelBuilder().for_address(host, rpc_port).make_secure(root_certificates=ca_filename).with_token_fetcher(token_fetcher).build(**kwargs)
