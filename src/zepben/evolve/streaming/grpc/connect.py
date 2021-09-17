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
import warnings
from typing import Optional

import grpc
from zepben.auth import ZepbenAuthenticator, create_authenticator

__all__ = ["connect", "connect_async"]
_AUTH_HEADER_KEY = 'authorization'

GRPC_READY_TIMEOUT = 5 # seconds


class AuthTokenPlugin(grpc.AuthMetadataPlugin):

    def __init__(self, authenticator: ZepbenAuthenticator):
        self.authenticator = authenticator

    def __call__(self, context, callback):
        token = self.authenticator.fetch_token()
        if token:
            callback(((_AUTH_HEADER_KEY, token),), None)
        else:
            callback()


def _conn(host: str = "localhost", rpc_port: int = 50051, conf_address: str = None, client_id: Optional[str] = None,
          username: Optional[str] = None, password: Optional[str] = None, client_secret: Optional[str] = None, pkey=None, cert=None, ca=None,
          authenticator: Optional[ZepbenAuthenticator] = None, secure: bool = False):
    """
    Connect to a Zepben gRPC service.

    `host` The host to connect to.
    `rpc_port` The gRPC port for host.

    `conf_address` The complete address for the auth configuration endpoint. This is used when an `authenticator` is not provided. Defaults to http://<host>/auth
    `secure` True if SSL is required, False otherwise (default). Must be True for authentication settings to be utilised.

    One of the following sets of arguments must be provided when authentication is configured on the server:
        `client_id` and `client_secret` for client credentials based authentication (usually M2M tokens), or
        `client_id`, `username`, and `password` for user credentials authentication. Note this is not recommended for untrusted and insecure servers as
        user credentials will be sent to the server in the clear. Or,
        `authenticator`, for custom connection options.

    `client_id` Your client id for your OAuth Auth provider.
    `client_secret` Corresponding client secret if required.

    `username` The username to use for an OAuth password grant.
    `password` Corresponding password. If both `username` and `password` are provided, it takes precedence over the above client credentials.

    `authenticator` An authenticator that can provide OAuth2 tokens the `host` can validate. If this is provided, it takes precedence over the above credentials.

    `pkey` Private key for client authentication if client authentication is required.
    `cert` Corresponding signed certificate if client authentication is required. CN must reflect your hosts FQDN, and must be signed by the servers CA.
    `ca` CA trust for the server, or None to use OS default certificate bundle.

    Raises `ConnectionError` if unable to make a connection to the server.
    Returns a gRPC channel
    """
    if secure:
        if conf_address is None:
            conf_address = f"http://{host}/auth"
        # Channel credential will be valid for the entire channel
        channel_credentials = grpc.ssl_channel_credentials(ca, pkey, cert)
        if authenticator:
            call_credentials = grpc.metadata_call_credentials(AuthTokenPlugin(authenticator=authenticator))

            # Combining channel credentials and call credentials together
            composite_credentials = grpc.composite_channel_credentials(
                channel_credentials,
                call_credentials,
            ) if channel_credentials else call_credentials
            channel = grpc.secure_channel(f"{host}:{rpc_port}", composite_credentials)
        elif client_id and username and password:
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
        elif client_id and client_secret:
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
        else:
            channel = grpc.secure_channel(f"{host}:{rpc_port}", channel_credentials)
    else:
        if client_id or client_secret or username or password or pkey or cert:
            warnings.warn("An insecure connection is being used but some credentials were specified for connecting, did you forget to set secure=True?")
        channel = grpc.insecure_channel(f"{host}:{rpc_port}")

    try:
        grpc.channel_ready_future(channel).result(timeout=GRPC_READY_TIMEOUT)
    except grpc.FutureTimeoutError as f:
        raise ConnectionError(f"Timed out connecting to server {host}:{rpc_port}")

    return channel


@contextlib.contextmanager
def connect(host: str = "localhost",
            rpc_port: int = 50051,
            conf_address: str = None,
            client_id: Optional[str] = None,
            client_secret: Optional[str] = None,
            username: Optional[str] = None,
            password: Optional[str] = None,
            pkey=None,
            cert=None,
            ca=None,
            authenticator: Optional[ZepbenAuthenticator] = None,
            secure=False):
    """
    Connect to a Zepben gRPC service.

    `host` The host to connect to.
    `rpc_port` The gRPC port for host.

    `conf_address` The complete address for the auth configuration endpoint. This is used when an `authenticator` is not provided. Defaults to http://<host>/auth
    `secure` True if SSL is required, False otherwise (default). Must be True for authentication settings to be utilised.

    One of the following sets of arguments must be provided when authentication is configured on the server:
        `client_id` and `client_secret` for client credentials based authentication (usually M2M tokens), or
        `client_id`, `username`, and `password` for user credentials authentication. Note this is not recommended for untrusted and insecure servers as
        user credentials will be sent to the server in the clear. Or,
        `authenticator`, for custom connection options.

    `client_id` Your client id for your OAuth Auth provider.
    `client_secret` Corresponding client secret if required.

    `username` The username to use for an OAuth password grant.
    `password` Corresponding password. If both `username` and `password` are provided, it takes precedence over the above client credentials.

    `authenticator` An authenticator that can provide OAuth2 tokens the `host` can validate. If this is provided, it takes precedence over the above credentials.

    `pkey` Private key for client authentication if client authentication is required.
    `cert` Corresponding signed certificate if client authentication is required. CN must reflect your hosts FQDN, and must be signed by the servers CA.
    `ca` CA trust for the server, or None to use OS default certificate bundle.

    Raises `ConnectionError` if unable to make a connection to the server.
    Returns a gRPC channel
    """
    yield _conn(host, rpc_port, conf_address, client_id, username, password, client_secret, pkey, cert, ca, authenticator, secure)


@contextlib.asynccontextmanager
async def connect_async(host: str = "localhost",
                        rpc_port: int = 50051,
                        conf_address: str = None,
                        client_id: Optional[str] = None,
                        client_secret: Optional[str] = None,
                        username: Optional[str] = None,
                        password: Optional[str] = None,
                        pkey=None,
                        cert=None,
                        ca=None,
                        authenticator: Optional[ZepbenAuthenticator] = None,
                        secure=False):
    """
    Connect to a Zepben gRPC service.

    `host` The host to connect to.
    `rpc_port` The gRPC port for host.

    `conf_address` The complete address for the auth configuration endpoint. This is used when an `authenticator` is not provided. Defaults to http://<host>/auth
    `secure` True if SSL is required, False otherwise (default). Must be True for authentication settings to be utilised.

    One of the following sets of arguments must be provided when authentication is configured on the server:
        `client_id` and `client_secret` for client credentials based authentication (usually M2M tokens), or
        `client_id`, `username`, and `password` for user credentials authentication. Note this is not recommended for untrusted and insecure servers as
        user credentials will be sent to the server in the clear. Or,
        `authenticator`, for custom connection options.

    `client_id` Your client id for your OAuth Auth provider.
    `client_secret` Corresponding client secret if required.

    `username` The username to use for an OAuth password grant.
    `password` Corresponding password. If both `username` and `password` are provided, it takes precedence over the above client credentials.

    `authenticator` An authenticator that can provide OAuth2 tokens the `host` can validate. If this is provided, it takes precedence over the above credentials.

    `pkey` Private key for client authentication if client authentication is required.
    `cert` Corresponding signed certificate if client authentication is required. CN must reflect your hosts FQDN, and must be signed by the servers CA.
    `ca` CA trust for the server, or None to use OS default certificate bundle.

    Raises `ConnectionError` if unable to make a connection to the server.
    Returns a gRPC channel
    """
    yield _conn(host, rpc_port, conf_address, client_id, username, password, client_secret, pkey, cert, ca, authenticator, secure)
