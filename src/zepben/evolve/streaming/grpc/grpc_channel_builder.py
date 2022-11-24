#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC
from typing import Optional

import grpc
from zepben.auth import ZepbenTokenFetcher

__all__ = ["GrpcChannelBuilder"]

from zepben.evolve.streaming.grpc.auth_token_plugin import AuthTokenPlugin


class GrpcChannelBuilder(ABC):
    """
    Builder class for gRPC channels to connect to EWB's gRPC service.
    """

    def __init__(self):
        self._socket_address: str = "localhost:50051"
        self._channel_credentials: Optional[grpc.ChannelCredentials] = None

    def build(self) -> grpc.aio.Channel:
        """
        Get the resulting :class:`grpc.aio.Channel` from this builder.
        :return: A gRPC channel resulting from this builder.
        """
        if self._channel_credentials:
            return grpc.aio.secure_channel(self._socket_address, self._channel_credentials)

        return grpc.aio.insecure_channel(self._socket_address)

    def for_address(self, host: str, port: int) -> 'GrpcChannelBuilder':
        """
        Specify the address for the gRPC channel.

        :param host: The hostname hosting the gRPC service
        :param port: The port of the gRPC service
        :return: This builder
        """
        self._socket_address = f"{host}:{port}"
        return self

    def make_secure(
        self,
        root_certificates: Optional[str] = None,
        certificate_chain: Optional[str] = None,
        private_key: Optional[str] = None
    ) -> 'GrpcChannelBuilder':
        """
        Secures channel with SSL credentials.

        :param root_certificates: The filename of the truststore to use when verifying the RPC service's SSL/TLS certificate
        :param certificate_chain: The filename of the certificate chain to use for client authentication
        :param private_key: The filename of the private key to use for client authentication
        :return: This builder
        """
        root_certificates_bytes = None
        if root_certificates is not None:
            with open(root_certificates, "rb") as f:
                root_certificates_bytes = f.read()

        certificate_chain_bytes = None
        if certificate_chain is not None:
            with open(certificate_chain, "rb") as f:
                certificate_chain_bytes = f.read()

        private_key_bytes = None
        if private_key is not None:
            with open(private_key, "rb") as f:
                private_key_bytes = f.read()

        return self.make_secure_with_bytes(root_certificates_bytes, certificate_chain_bytes, private_key_bytes)

    def make_secure_with_bytes(
        self,
        root_certificates_bytes: Optional[bytes] = None,
        certificate_chain_bytes: Optional[bytes] = None,
        private_key_bytes: Optional[bytes] = None
    ) -> 'GrpcChannelBuilder':
        """
        Secures channel with SSL credentials.

        :param root_certificates_bytes: The bytestring truststore to use when verifying the RPC service's SSL/TLS certificate
        :param certificate_chain_bytes: The bytestring certificate chain to use for client authentication
        :param private_key_bytes: The bytestring private key to use for client authentication
        :return: This builder
        """
        self._channel_credentials = grpc.ssl_channel_credentials(root_certificates_bytes, private_key_bytes, certificate_chain_bytes)
        return self

    def with_token_fetcher(self, token_fetcher: ZepbenTokenFetcher) -> 'GrpcChannelBuilder':
        """
        Authenticates calls for the gRPC channel using a :class:`ZepbenTokenFetcher`.

        :param token_fetcher: The :class:`ZepbenTokenFetcher` to use to fetch access tokens.
        :return: This builder
        """
        if self._channel_credentials is None:
            raise Exception("You must call make_secure before calling with_token_fetcher.")
        self._channel_credentials = grpc.composite_channel_credentials(
            self._channel_credentials,
            grpc.metadata_call_credentials(AuthTokenPlugin(token_fetcher=token_fetcher))
        )
        return self
