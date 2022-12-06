#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional, Union

import grpc
from zepben.auth import ZepbenTokenFetcher, create_token_fetcher
from zepben.evolve import GrpcChannelBuilder

__all__ = ["connect_tls", "connect_insecure", "connect_with_password", "connect_with_secret"]

GRPC_READY_TIMEOUT = 20  # seconds


def connect_insecure(
    host: str = "localhost",
    rpc_port: int = 50051
) -> grpc.aio.Channel:
    """
    Create a :class:`grpc.aio.Channel` that communicates with the gRPC service over plaintext.

    :param host: The hostname where the gRPC service is hosted
    :param rpc_port: The port of the gRPC service
    :return: A plaintext connection to the gRPC service
    """
    return GrpcChannelBuilder().for_address(host, rpc_port).build()


def connect_tls(
    host: str = "localhost",
    rpc_port: int = 50051,
    ca_filename: Optional[str] = None
) -> grpc.aio.Channel:
    """
    Create a :class:`grpc.aio.Channel` that communicates with the gRPC service using SSL/TLS transport security.

    :param host: The hostname where the gRPC service is hosted
    :param rpc_port: The port of the gRPC service
    :param ca_filename: The filename of a truststore containing additional trusted root certificates. This parameter is optional
                        and defaults to null, in which case only the system CAs are used to verify certificates.
    :return:An encrypted connection to the gRPC service
    """
    return GrpcChannelBuilder().for_address(host, rpc_port).make_secure(root_certificates=ca_filename).build()


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
    :param verify_auth: Passed through to `requests.post()` when fetching access tokens
    :param ca_filename: The filename of a truststore containing additional trusted root certificates. This parameter is optional
                        and defaults to null, in which case only the system CAs are used to verify certificates.
    :param kwargs: If `audience: str` and `issuer_domain: str` are specified, `kwargs` will be used as parameters
                   to construct the :class:`ZepbenTokenFetcher` directly.
    :return: An Auth0-authenticated, encrypted connection to the gRPC service. If the authentication configuration specifies that no authentication is
             required, a non-authenticated, encrypted connection is returned instead.
    """
    if {"audience", "issuer_domain"} <= kwargs.keys():
        # noinspection PyArgumentList
        token_fetcher = ZepbenTokenFetcher(**kwargs)
    else:
        token_fetcher = create_token_fetcher(
            conf_address=conf_address or f"https://{host}/ewb/auth",
            verify_conf=verify_conf,
            verify_auth=verify_auth
        )

    if token_fetcher:
        return _connect_with_secret_using_token_fetcher(token_fetcher, client_id, client_secret, host, rpc_port, ca_filename)
    else:
        return connect_tls(host, rpc_port, ca_filename)


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
    :param verify_auth: Passed through to `requests.post()` when fetching access tokens
    :param ca_filename: The filename of a truststore containing additional trusted root certificates. This parameter is optional
                        and defaults to null, in which case only the system CAs are used to verify certificates.
    :param kwargs: If `audience: str` and `issuer_domain: str` are specified, `kwargs` will be used as parameters
                   to construct the :class:`ZepbenTokenFetcher` directly.
    :return: An Auth0-authenticated, encrypted connection to the gRPC service. If the authentication configuration specifies that no authentication is
             required, a non-authenticated, encrypted connection is returned instead.
    """
    if {"audience", "issuer_domain"} <= kwargs.keys():
        # noinspection PyArgumentList
        token_fetcher = ZepbenTokenFetcher(**kwargs)
    else:
        token_fetcher = create_token_fetcher(
            conf_address=conf_address or f"https://{host}/ewb/auth",
            verify_conf=verify_conf,
            verify_auth=verify_auth
        )

    if token_fetcher:
        return _connect_with_password_using_token_fetcher(token_fetcher, client_id, username, password, host, rpc_port, ca_filename)
    else:
        return connect_tls(host, rpc_port, ca_filename)


def _connect_with_secret_using_token_fetcher(
    token_fetcher: ZepbenTokenFetcher,
    client_id: str,
    client_secret: str,
    host: str,
    rpc_port: int,
    ca_filename: Optional[str]
) -> grpc.aio.Channel:
    token_fetcher.token_request_data["client_id"] = client_id
    token_fetcher.token_request_data["client_secret"] = client_secret
    token_fetcher.token_request_data["grant_type"] = "client_credentials"

    return GrpcChannelBuilder().for_address(host, rpc_port).make_secure(root_certificates=ca_filename).with_token_fetcher(token_fetcher).build()


def _connect_with_password_using_token_fetcher(
    token_fetcher: ZepbenTokenFetcher,
    client_id: str,
    username: str,
    password: str,
    host: str,
    rpc_port: int,
    ca_filename: Optional[str]
) -> grpc.aio.Channel:
    token_fetcher.token_request_data["client_id"] = client_id
    token_fetcher.token_request_data["username"] = username
    token_fetcher.token_request_data["password"] = password
    token_fetcher.token_request_data["grant_type"] = "password"
    token_fetcher.token_request_data["scope"] = "offline_access"

    return GrpcChannelBuilder().for_address(host, rpc_port).make_secure(root_certificates=ca_filename).with_token_fetcher(token_fetcher).build()
