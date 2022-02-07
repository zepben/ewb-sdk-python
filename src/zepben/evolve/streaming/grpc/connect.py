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
from zepben.auth.client import ZepbenTokenFetcher, AuthMethod

from zepben.evolve import GrpcChannelBuilder

__all__ = ["connect_with_password", "connect_with_password_async"]
GRPC_READY_TIMEOUT = 5.0


def _secure_grpc_channel_builder(host: str = "localhost", rpc_port: int = 50051) -> GrpcChannelBuilder:
    return GrpcChannelBuilder() \
        .socket_address(host, rpc_port) \
        .make_secure()


def _grpc_channel_builder_from_password(client_id: str, username: str, password: str, host: str, rpc_port: int) -> GrpcChannelBuilder:
    # noinspection PyArgumentList
    token_fetcher = ZepbenTokenFetcher(
        audience="https://evolve-ewb/",
        issuer_domain="zepben.au.auth0.com",
        auth_method=AuthMethod.AUTH0,
        verify_certificate=True,
        token_request_data={
            'client_id': client_id,
            'username': username,
            'password': password,
            'grant_type': 'password',
            'scope': 'offline_access'
        }
    )

    return GrpcChannelBuilder() \
        .socket_address(host, rpc_port) \
        .make_secure() \
        .token_fetcher(token_fetcher)


@contextlib.contextmanager
def connect(host: str = "localhost", rpc_port: int = 50051, timeout: float = GRPC_READY_TIMEOUT) -> grpc.Channel:
    yield _secure_grpc_channel_builder(host, rpc_port).connect(timeout)


@contextlib.asynccontextmanager
def connect_async(host: str = "localhost", rpc_port: int = 50051, timeout: float = GRPC_READY_TIMEOUT) -> grpc.Channel:
    yield _secure_grpc_channel_builder(host, rpc_port).connect(timeout)


@contextlib.contextmanager
def connect_with_password(client_id: str, username: str, password: str, host: str = "localhost", rpc_port: int = 50051,
                          timeout: float = GRPC_READY_TIMEOUT) -> grpc.Channel:
    yield _grpc_channel_builder_from_password(client_id, username, password, host, rpc_port).connect(timeout)


@contextlib.asynccontextmanager
def connect_with_password_async(client_id: str, username: str, password: str, host: str = "localhost", rpc_port: int = 50051,
                                timeout: float = GRPC_READY_TIMEOUT) -> grpc.Channel:
    yield _grpc_channel_builder_from_password(client_id, username, password, host, rpc_port).connect(timeout)
