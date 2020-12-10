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
import grpc
import requests
import json
from jose import jwt
from datetime import datetime
from zepben.evolve.streaming.exceptions import AuthException

__all__ = ["connect", "connect_async"]
_AUTH_HEADER_KEY = 'authorization'


class AuthTokenPlugin(grpc.AuthMetadataPlugin):

    def __init__(self, host, conf_address, client_id, client_secret):
        self.host = host
        self.conf_address = conf_address
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = ""
        self.token_expiry = 0
        self._refresh_token()

    def __call__(self, context, callback):
        if datetime.utcnow().timestamp() > self.token_expiry:
            self._refresh_token()
        callback(((_AUTH_HEADER_KEY, self.token),), None)

    def _refresh_token(self):
        parts = get_token(self.host, self.conf_address, self.client_id, self.client_secret)
        self.token = f"{parts['token_type']} {parts['access_token']}"
        self.token_expiry = jwt.get_unverified_claims(parts['access_token'])['exp']


def get_token(addr, conf_address, client_id, client_secret):
    # Get the configuration TODO: this probably needs to be OAuth2 compliant or something
    with requests.session() as session:
        with session.get(conf_address) as resp:
            result = json.loads(resp.text)
            domain = result["dom"]
            aud = result["aud"]
        with session.post(domain, data={'client_id': client_id, 'client_secret': client_secret, 'audience': aud, 'grant_type': 'client_credentials'}) as resp:
            token = json.loads(resp.text)
    if 'error' in token:
        raise AuthException(f"{token['error']}: {token['error_description']}")
    return token


def _conn(host: str = "localhost", rpc_port: int = 50051, conf_address: str = "http://localhost/auth", client_id: str = None,
          client_secret: str = None, pkey=None, cert=None, ca=None):
    """
    `host` The host to connect to.
    `rpc_port` The gRPC port for host.
    `conf_address` The complete address for the auth configuration endpoint.
    `client_id` Your client id for your OAuth Auth provider.
    `client_secret` Corresponding client secret.
    `pkey` Private key for client authentication
    `cert` Corresponding signed certificate. CN must reflect your hosts FQDN, and must be signed by the servers
                 CA.
    `ca` CA trust for the server.
    `secure_conf` Whether the server hosting configuration is secured (https)
    Returns A gRPC channel
    """
    # TODO: make this more robust so it can handle SSL without client verification
    if pkey and cert and client_id and client_secret:
        call_credentials = grpc.metadata_call_credentials(AuthTokenPlugin(host, conf_address, client_id, client_secret))
        # Channel credential will be valid for the entire channel
        channel_credentials = grpc.ssl_channel_credentials(ca, pkey, cert)
        # Combining channel credentials and call credentials together
        composite_credentials = grpc.composite_channel_credentials(
            channel_credentials,
            call_credentials,
        )
        channel = grpc.secure_channel(f"{host}:{rpc_port}", composite_credentials)
    else:
        channel = grpc.insecure_channel(f"{host}:{rpc_port}")

    return channel


@contextlib.contextmanager
def connect(host: str = "localhost",
            rpc_port: int = 50051,
            conf_address: str = "http://localhost/auth",
            client_id: str = None,
            client_secret: str = None,
            pkey=None,
            cert=None,
            ca=None):
    """
    Usage:
        with connect(args) as channel:

    `host` The host to connect to.
    `rpc_port` The gRPC port for host.
    `conf_address` The complete address for the auth configuration endpoint.
    `client_id` Your client id for your OAuth Auth provider.
    `client_secret` Corresponding client secret.
    `pkey` Private key for client authentication
    `cert` Corresponding signed certificate. CN must reflect your hosts FQDN, and must be signed by the servers
                 CA.
    `ca` CA trust for the server.
    Returns A gRPC channel
    """
    yield _conn(host, rpc_port, conf_address, client_id, client_secret, pkey, cert, ca)


@contextlib.asynccontextmanager
async def connect_async(host: str = "localhost",
                        rpc_port: int = 50051,
                        conf_address: str = "http://localhost/auth",
                        client_id: str = None,
                        client_secret: str = None,
                        pkey=None,
                        cert=None,
                        ca=None):
    """
    Usage:
        async with connect_async(args) as channel:

    `host` The host to connect to.
    `rpc_port` The gRPC port for host.
    `conf_address` The complete address for the auth configuration endpoint.
    `client_id` Your client id for your OAuth Auth provider.
    `client_secret` Corresponding client secret.
    `pkey` Private key for client authentication
    `cert` Corresponding signed certificate. CN must reflect your hosts FQDN, and must be signed by the servers
                 CA.
    `ca` CA trust for the server.
    Returns A gRPC channel
    """
    yield _conn(host, rpc_port, conf_address, client_id, client_secret, pkey, cert, ca)
