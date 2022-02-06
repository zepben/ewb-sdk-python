#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import contextlib
from abc import ABC
from typing import Optional

import grpc
from zepben.auth.client import ZepbenTokenFetcher

from zepben.evolve.streaming.grpc.connect import AuthTokenPlugin


class GrpcChannelBuilder(ABC):

    def __init__(self):
        self._socket_address: str = "localhost:50051"
        self._channel_credentials: Optional[grpc.ChannelCredentials] = None

    def _build(self) -> grpc.Channel:
        if self._channel_credentials:
            return grpc.secure_channel(self._socket_address, self._channel_credentials)

        return grpc.insecure_channel(self._socket_address)

    def _conn(self, timeout):
        channel = self._build()
        try:
            grpc.channel_ready_future(channel).result(timeout=timeout)
        except grpc.FutureTimeoutError:
            raise ConnectionError(f"Timed out connecting to server {self._socket_address}")
        return channel

    @contextlib.contextmanager
    def connect(self, timeout=5) -> grpc.Channel:
        yield self._conn(timeout)

    @contextlib.asynccontextmanager
    async def connect_async(self, timeout=5) -> grpc.Channel:
        yield self._conn(timeout)

    def socket_address(self, host: str, port: int) -> 'GrpcChannelBuilder':
        self._socket_address = f"{host}:{port}"
        return self

    def make_secure(
        self,
        root_certificates: Optional[bytes] = None,
        private_key: Optional[bytes] = None,
        certificate_chain: Optional[bytes] = None
    ) -> 'GrpcChannelBuilder':
        """
        Secures channel with SSL credentials.
        """
        self._channel_credentials = grpc.ssl_channel_credentials(root_certificates, private_key, certificate_chain)
        return self

    def token_fetcher(self, token_fetcher: ZepbenTokenFetcher) -> 'GrpcChannelBuilder':
        if self._channel_credentials is None:
            raise Exception("Attempted to set call credentials before channel credentials.")
        self._channel_credentials = grpc.composite_channel_credentials(
            self._channel_credentials,
            grpc.metadata_call_credentials(AuthTokenPlugin(token_fetcher=token_fetcher))
        )
        return self
