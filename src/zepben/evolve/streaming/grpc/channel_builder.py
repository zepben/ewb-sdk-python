#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC
from typing import Optional

import grpc
from zepben.auth.client import ZepbenTokenFetcher

__all__ = ["GrpcChannelBuilder", "AuthTokenPlugin"]
_AUTH_HEADER_KEY = 'authorization'


class AuthTokenPlugin(grpc.AuthMetadataPlugin):

    def __init__(self, token_fetcher: ZepbenTokenFetcher):
        self.token_fetcher = token_fetcher

    def __call__(self, context, callback):
        token = self.token_fetcher.fetch_token()
        if token:
            callback(((_AUTH_HEADER_KEY, token),), None)
        else:
            callback()


class GrpcChannelBuilder(ABC):

    def __init__(self):
        self._socket_address: str = "localhost:50051"
        self._channel_credentials: Optional[grpc.ChannelCredentials] = None

    def build(self) -> grpc.aio.Channel:
        if self._channel_credentials:
            return grpc.aio.secure_channel(self._socket_address, self._channel_credentials)

        return grpc.aio.insecure_channel(self._socket_address)

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
