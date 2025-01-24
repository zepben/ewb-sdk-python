#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC
from typing import Optional, List, Tuple, Any, Dict

import grpc
from grpc._channel import _InactiveRpcError
from zepben.auth import ZepbenTokenFetcher
from zepben.protobuf.cc.cc_pb2_grpc import CustomerConsumerStub
from zepben.protobuf.connection.connection_requests_pb2 import CheckConnectionRequest
from zepben.protobuf.dc.dc_pb2_grpc import DiagramConsumerStub
from zepben.protobuf.nc.nc_pb2_grpc import NetworkConsumerStub
from zepben.protobuf.ns.network_state_pb2_grpc import QueryNetworkStateServiceStub, UpdateNetworkStateServiceStub

from zepben.evolve.streaming.exceptions import GrpcConnectionException
from zepben.evolve.streaming.grpc.auth_token_plugin import AuthTokenPlugin

__all__ = ["GrpcChannelBuilder"]

_TWENTY_MEGABYTES = 1024 * 1024 * 20


class GrpcChannelBuilder(ABC):
    """
    Builder class for gRPC channels to connect to EWB's gRPC service.
    """

    _stubs: Dict = {
        "NetworkConsumerClient": NetworkConsumerStub,
        "DiagramConsumerClient": DiagramConsumerStub,
        "CustomerConsumerClient": CustomerConsumerStub,
        "QueryNetworkStateClient": QueryNetworkStateServiceStub,
        "UpdateNetworkStateClient": UpdateNetworkStateServiceStub
    }

    def __init__(self):
        self._socket_address: str = "localhost:50051"
        self._channel_credentials: Optional[grpc.ChannelCredentials] = None

    def build(self, skip_connection_test: bool = False, timeout_seconds: int = 5, debug: bool = False,
              options: Optional[List[Tuple[str, Any]]] = None) -> grpc.aio.Channel:
        """
        Get the resulting :class:`grpc.aio.Channel` from this builder.

        :param skip_connection_test: Skip confirming a connection can be established to the server. This is not recommended, but provided as a safety
        mechanism if for any reason the connection test fails unexpectedly even though the connection is fine.
        :param timeout_seconds: The timeout used for each request made in the connection test.
        :param debug: Collect and append unhandled RPC errors to the `ConnectionException` raised on an unsuccessful connection test.
        :param options: An optional list of key-value pairs (channel_arguments in gRPC Core runtime) to configure the channel.

        :return: A gRPC channel resulting from this builder.
        """

        # Synchronous channel is used purely for confirming channel connection works as we can't do async requests here,
        # but an aio channel is always returned to the user.
        if not skip_connection_test:
            if self._channel_credentials:
                channel = grpc.secure_channel(self._socket_address, self._channel_credentials)
            else:
                channel = grpc.insecure_channel(self._socket_address)
            self._test_connection(channel, debug=debug, timeout_seconds=timeout_seconds)
            channel.close()

        if options is None:
            options = [("grpc.max_receive_message_length", _TWENTY_MEGABYTES), ("grpc.max_send_message_length", _TWENTY_MEGABYTES)]
        else:
            has_max_receive_msg_length = False
            has_max_send_msg_length = False
            for key, _ in options:
                if key == "grpc.max_receive_message_length":
                    has_max_receive_msg_length = True
                if key == "grpc.max_send_message_length":
                    has_max_send_msg_length = True
            if not has_max_send_msg_length:
                options.append(("grpc.max_send_message_length", _TWENTY_MEGABYTES))
            if not has_max_receive_msg_length:
                options.append(("grpc.max_receive_message_length", _TWENTY_MEGABYTES))

        if self._channel_credentials:
            return grpc.aio.secure_channel(self._socket_address, self._channel_credentials, options=options)

        return grpc.aio.insecure_channel(self._socket_address, options=options)

    def _test_connection(self, channel: grpc.Channel, debug: bool, timeout_seconds: int):
        debug_errors = []
        for name, client in zip(self._stubs.keys(), map(lambda stub: stub(channel), list(self._stubs.values()))):
            try:
                result = client.checkConnection(CheckConnectionRequest(), timeout=timeout_seconds, wait_for_ready=False)
                if result:
                    return
            except _InactiveRpcError as rpc_error:
                debug_errors.append(f"Received the following exception with {name}:\n{rpc_error}\n")
        raise GrpcConnectionException(f"Couldn't establish gRPC connection to any service on {self._socket_address}.\n{''.join(debug_errors) if debug else ''}")

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

    def with_client_token(self, client_token: str) -> 'GrpcChannelBuilder':
        """
        Authenticates calls for the gRPC channel using a client access token string.

        :param client_token: The :class:`str` that has been generated in Evolve application.
        :return: This builder
        """
        if self._channel_credentials is None:
            raise Exception("You must call make_secure before calling with_client_token.")
        self._channel_credentials = grpc.composite_channel_credentials(
            self._channel_credentials,
            grpc.access_token_call_credentials(client_token)
        )
        return self
