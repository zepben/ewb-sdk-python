#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import contextlib
from typing import Optional

import grpc
from zepben.auth import ZepbenAuthenticator, create_authenticator

__all__ = ["connect", "connect_async"]
_AUTH_HEADER_KEY = 'authorization'


class AuthTokenPlugin(grpc.AuthMetadataPlugin):

    def __init__(self, authenticator: ZepbenAuthenticator):
        self.authenticator = authenticator

    def __call__(self, context, callback):
        token = self.authenticator.fetch_token()
        if token:
            callback(((_AUTH_HEADER_KEY, token),), None)
        else:
            callback()


def _conn(host: str = "localhost", rpc_port: int = 50051, conf_address: str = "http://localhost/auth", client_id: Optional[str] = None,
          username: Optional[str] = None, password: Optional[str] = None, client_secret: Optional[str] = None, pkey=None, cert=None, ca=None,
          authenticator: Optional[ZepbenAuthenticator] = None):
    """
    `host` The host to connect to.
    `rpc_port` The gRPC port for host.
    `conf_address` The complete address for the auth configuration endpoint. This is used when an `authenticator` is not provided.

    One of the following sets of arguments must be provided:
        `client_id` and `client_secret` for client credentials based authentication (usually M2M tokens), or
        `client_id`, `username`, and `password` for user credentials authentication. Note this is not recommended for untrusted and insecure servers as
        user credentials will be sent to the server in the clear. Or,
        `authenticator`, for custom connection options.

    `client_id` Your client id for your OAuth Auth provider.
    `client_secret` Corresponding client secret if required.

    `username` The username to use for an OAuth password grant.
    `password` Corresponding password. If both `username` and `password` are provided, it takes precedence over the above client credentials.

    `authenticator` An authenticator that can provide OAuth2 tokens the `host` can validate. If this is provided, it takes precedence over the above credentials.

    `pkey` Private key for client authentication
    `cert` Corresponding signed certificate. CN must reflect your hosts FQDN, and must be signed by the servers CA.
    `ca` CA trust for the server.

    Raises `ValueError` upon incompatible arguments.
    Returns a gRPC channel
    """
    # Channel credential will be valid for the entire channel
    channel_credentials = grpc.ssl_channel_credentials(ca, pkey, cert) if ca else None
    # TODO: make this more robust so it can handle SSL without client verification
    if ca and authenticator:
        call_credentials = grpc.metadata_call_credentials(AuthTokenPlugin(authenticator=authenticator))

        # Combining channel credentials and call credentials together
        composite_credentials = grpc.composite_channel_credentials(
            channel_credentials,
            call_credentials,
        ) if channel_credentials else call_credentials
        channel = grpc.secure_channel(f"{host}:{rpc_port}", composite_credentials)
    elif ca and client_id and username and password:
        # Create a basic ClientCredentials authenticator
        authenticator = create_authenticator(conf_address)
        authenticator.token_request_data.update({
            'client_id': client_id,
            'username': username,
            'password': password,
            'grant_type': 'password',
            'scope': 'offline_access'
        })

        call_credentials = grpc.metadata_call_credentials(AuthTokenPlugin(authenticator))

        # Combining channel credentials and call credentials together
        composite_credentials = grpc.composite_channel_credentials(
            channel_credentials,
            call_credentials,
        ) if channel_credentials else call_credentials
        channel = grpc.secure_channel(f"{host}:{rpc_port}", composite_credentials)
    elif ca and client_id and client_secret:
        # Create a basic ClientCredentials authenticator
        authenticator = create_authenticator(conf_address)
        authenticator.token_request_data.update({'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'client_credentials'})

        call_credentials = grpc.metadata_call_credentials(AuthTokenPlugin(authenticator))

        # Combining channel credentials and call credentials together
        composite_credentials = grpc.composite_channel_credentials(
            channel_credentials,
            call_credentials,
        ) if channel_credentials else call_credentials
        channel = grpc.secure_channel(f"{host}:{rpc_port}", composite_credentials)
    elif ca and (not client_id and not client_secret and not authenticator):
        channel = grpc.secure_channel(f"{host}:{rpc_port}", channel_credentials)
    elif not ca and not client_secret and not client_id and not pkey and not cert and not authenticator:
        channel = grpc.insecure_channel(f"{host}:{rpc_port}")
    else:
        raise ValueError("Incompatible arguments passed to connect. You must specify at least (client_id, username, password, ca),"
                         "(client_id, client_secret, ca) or (authenticator, ca) for a secure connection with token based auth.")

    return channel


@contextlib.contextmanager
def connect(host: str = "localhost",
            rpc_port: int = 50051,
            conf_address: str = "http://localhost/auth",
            client_id: Optional[str] = None,
            client_secret: Optional[str] = None,
            username: Optional[str] = None,
            password: Optional[str] = None,
            pkey=None,
            cert=None,
            ca=None,
            authenticator: Optional[ZepbenAuthenticator] = None):
    """
    Usage:
        with connect(args) as channel:

    `host` The host to connect to.
    `rpc_port` The gRPC port for host.
    `conf_address` The complete address for the auth configuration endpoint. This is used when an `authenticator` is not provided.

    One of the following sets of arguments must be provided:
        `client_id` and `client_secret` for client credentials based authentication (usually M2M tokens), or
        `client_id`, `username`, and `password` for user credentials authentication. Note this is not recommended for untrusted and insecure servers as
        user credentials will be sent to the server in the clear. Or,
        `authenticator`, for custom connection options.

    `client_id` Your client id for your OAuth Auth provider.
    `client_secret` Corresponding client secret if required.

    `username` The username to use for an OAuth password grant.
    `password` Corresponding password. If both `username` and `password` are provided, it takes precedence over the above client credentials.

    `authenticator` An authenticator that can provide OAuth2 tokens the `host` can validate. If this is provided, it takes precedence over the above credentials.

    `pkey` Private key for client authentication
    `cert` Corresponding signed certificate. CN must reflect your hosts FQDN, and must be signed by the servers CA.
    `ca` CA trust for the server.

    Raises `ValueError` upon incompatible arguments.
    Returns a gRPC channel
    """
    yield _conn(host, rpc_port, conf_address, client_id, username, password, client_secret, pkey, cert, ca, authenticator)


@contextlib.asynccontextmanager
async def connect_async(host: str = "localhost",
                        rpc_port: int = 50051,
                        conf_address: str = "http://localhost/auth",
                        client_id: Optional[str] = None,
                        client_secret: Optional[str] = None,
                        username: Optional[str] = None,
                        password: Optional[str] = None,
                        pkey=None,
                        cert=None,
                        ca=None,
                        authenticator: Optional[ZepbenAuthenticator] = None):
    """
    Usage:
        async with connect_async(args) as channel:

    `host` The host to connect to.
    `rpc_port` The gRPC port for host.
    `conf_address` The complete address for the auth configuration endpoint. This is used when an `authenticator` is not provided.

    One of the following sets of arguments must be provided:
        `client_id` and `client_secret` for client credentials based authentication (usually M2M tokens), or
        `client_id`, `username`, and `password` for user credentials authentication. Note this is not recommended for untrusted and insecure servers as
        user credentials will be sent to the server in the clear. Or,
        `authenticator`, for custom connection options.

    `client_id` Your client id for your OAuth Auth provider.
    `client_secret` Corresponding client secret if required.

    `username` The username to use for an OAuth password grant.
    `password` Corresponding password. If both `username` and `password` are provided, it takes precedence over the above client credentials.

    `authenticator` An authenticator that can provide OAuth2 tokens the `host` can validate. If this is provided, it takes precedence over the above credentials.

    `pkey` Private key for client authentication
    `cert` Corresponding signed certificate. CN must reflect your hosts FQDN, and must be signed by the servers CA.
    `ca` CA trust for the server.

    Raises `ValueError` upon incompatible arguments.
    Returns a gRPC channel
    """
    yield _conn(host, rpc_port, conf_address, client_id, username, password, client_secret, pkey, cert, ca, authenticator)
