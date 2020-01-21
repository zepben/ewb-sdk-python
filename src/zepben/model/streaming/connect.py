"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""


import contextlib
import grpc
import requests
import json
from jose import jwt
from datetime import datetime
from zepben.model.streaming.exceptions import AuthException
from zepben.model.streaming.api import WorkbenchConnection
from zepben.model.streaming.sync_api import SyncWorkbenchConnection

__all__ = ["connect", "connect_async"]
_AUTH_HEADER_KEY = 'authorization'


class AuthTokenPlugin(grpc.AuthMetadataPlugin):

    def __init__(self, host, port, client_id, client_secret):
        self.host = host
        self.port = port
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
        parts = get_token(self.host, self.port, self.client_id, self.client_secret)
        self.token = f"{parts['token_type']} {parts['access_token']}"
        self.token_expiry = jwt.get_unverified_claims(parts['access_token'])['exp']


def get_token(addr, port, client_id, client_secret):
    # Get the configuration TODO: this probably needs to be OAuth2 compliant or something
    with requests.session() as session:
        with session.get(f"http://{addr}:{port}/auth") as resp:
            result = json.loads(resp.text)
            domain = result["dom"]
            aud = result["aud"]
        with session.post(domain, data={'client_id': client_id, 'client_secret': client_secret, 'audience': aud, 'grant_type': 'client_credentials'}) as resp:
            token = json.loads(resp.text)
    if 'error' in token:
        raise AuthException(f"{token['error']}: {token['error_description']}")
    return token


def _conn(host: str = "localhost", rpc_port: int = 50051, conf_port: int = 80, client_id: str = None,
          client_secret: str = None, pkey=None, cert=None, ca=None):
    """
    :param host: The host to connect to.
    :param rpc_port: The gRPC port for host.
    :param conf_port: The configuration port for host.
    :param client_id: Your client id for your OAuth Auth provider.
    :param client_secret: Corresponding client secret.
    :param pkey: Private key for client authentication
    :param cert: Corresponding signed certificate. CN must reflect your hosts FQDN, and must be signed by the servers
                 CA.
    :param ca: CA trust for the server.
    :return: A gRPC channel
    """
    # TODO: make this more robust so it can handle SSL without client verification
    if pkey and cert and client_id and client_secret:
        call_credentials = grpc.metadata_call_credentials(AuthTokenPlugin(host, conf_port, client_id, client_secret))
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
            conf_port: int = 80,
            client_id: str = None,
            client_secret: str = None,
            pkey=None,
            cert=None,
            ca=None):
    """
    Usage:
        with connect(args) as channel:

    :param host: The host to connect to.
    :param rpc_port: The gRPC port for host.
    :param conf_port: The configuration port for host.
    :param client_id: Your client id for your OAuth Auth provider.
    :param client_secret: Corresponding client secret.
    :param pkey: Private key for client authentication
    :param cert: Corresponding signed certificate. CN must reflect your hosts FQDN, and must be signed by the servers
                 CA.
    :param ca: CA trust for the server.
    :return: A gRPC channel
    """
    with _conn(host, rpc_port, conf_port, client_id, client_secret, pkey, cert, ca) as channel:
        conn = SyncWorkbenchConnection(channel)
        yield conn


@contextlib.asynccontextmanager
async def connect_async(host: str = "localhost",
                        rpc_port: int = 50051,
                        conf_port: int = 80,
                        client_id: str = None,
                        client_secret: str = None,
                        pkey=None,
                        cert=None,
                        ca=None):
    """
    Usage:
        async with connect_async(args) as channel:

    :param host: The host to connect to.
    :param rpc_port: The gRPC port for host.
    :param conf_port: The configuration port for host.
    :param client_id: Your client id for your OAuth Auth provider.
    :param client_secret: Corresponding client secret.
    :param pkey: Private key for client authentication
    :param cert: Corresponding signed certificate. CN must reflect your hosts FQDN, and must be signed by the servers
                 CA.
    :param ca: CA trust for the server.
    :return: A gRPC channel
    """
    with _conn(host, rpc_port, conf_port, client_id, client_secret, pkey, cert, ca) as channel:
        conn = WorkbenchConnection(channel)
        yield conn
