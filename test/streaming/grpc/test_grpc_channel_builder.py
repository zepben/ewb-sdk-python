#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest import mock
from unittest.mock import call

import pytest
from zepben.protobuf.connection.connection_requests_pb2 import CheckConnectionRequest

from test.util import all_subclasses
from zepben.ewb.dataclassy import dataclass
from grpc import StatusCode, insecure_channel
from grpc._channel import _InactiveRpcError, _RPCState
from grpc._cython.cygrpc import OperationType
from zepben.ewb.auth import ZepbenTokenFetcher

from zepben.ewb import GrpcChannelBuilder, GrpcConnectionException, GrpcClient

_TWENTY_MEGABYTES = 1024 * 1024 * 20
DEFAULT_GRPC_CHANNEL_MAX_RECEIVE_MESSAGE_LENGTH = ("grpc.max_receive_message_length", _TWENTY_MEGABYTES)
DEFAULT_GRPC_CHANNEL_MAX_SEND_MESSAGE_LENGTH = ("grpc.max_send_message_length", _TWENTY_MEGABYTES)
DEFAULT_GRPC_CHANNEL_OPTIONS = [DEFAULT_GRPC_CHANNEL_MAX_RECEIVE_MESSAGE_LENGTH, DEFAULT_GRPC_CHANNEL_MAX_SEND_MESSAGE_LENGTH]


@dataclass
class MockReadable:
    contents: bytes

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def read(self):
        return self.contents


@dataclass
class MockedChannel:
    """
    Mocked `grpc.insecure_channel`/`secure_channel` returns this class to represent the sync channel to be passed to `_test_connection()` rather than just a
    string like the mocked `grpc.aio.insecure_channel` because we call `close()` on the sync channel inside `build()` after we are finished testing with it.
    """
    name: str

    def close(self):
        pass


@mock.patch("zepben.ewb.GrpcChannelBuilder._test_connection")
@mock.patch("grpc.aio.insecure_channel", return_value="insecure channel")
def test_skip_connection_test(mock_insecure_channel, mock_test_connection):
    assert GrpcChannelBuilder().build(skip_connection_test=True) == "insecure channel"

    mock_insecure_channel.assert_called_once_with('localhost:50051', options=DEFAULT_GRPC_CHANNEL_OPTIONS)
    mock_test_connection.assert_not_called()


@mock.patch("grpc.insecure_channel", return_value=MockedChannel('insecure sync test channel'))
@mock.patch("zepben.ewb.GrpcChannelBuilder._test_connection")
@mock.patch("grpc.aio.insecure_channel", return_value="insecure channel")
def test_debug_connection_test(mock_insecure_channel, mock_test_connection, mock_insecure_sync_channel):
    assert GrpcChannelBuilder().build(debug=True) == "insecure channel"

    mock_insecure_sync_channel.assert_called_once_with("localhost:50051")
    mock_test_connection.assert_called_once_with(MockedChannel('insecure sync test channel'), debug=True, timeout_seconds=5)
    mock_insecure_channel.assert_called_once_with('localhost:50051', options=DEFAULT_GRPC_CHANNEL_OPTIONS)


@mock.patch("grpc.insecure_channel", return_value=MockedChannel('insecure sync test channel'))
@mock.patch("zepben.ewb.GrpcChannelBuilder._test_connection")
@mock.patch("grpc.aio.insecure_channel", return_value="insecure channel")
def test_timeout_connection_test(mock_insecure_channel, mock_test_connection, mock_insecure_sync_channel):
    assert GrpcChannelBuilder().build(timeout_seconds=2789) == "insecure channel"

    mock_insecure_sync_channel.assert_called_once_with("localhost:50051")
    mock_test_connection.assert_called_once_with(MockedChannel('insecure sync test channel'), debug=False, timeout_seconds=2789)
    mock_insecure_channel.assert_called_once_with('localhost:50051', options=DEFAULT_GRPC_CHANNEL_OPTIONS)


@mock.patch("grpc.insecure_channel", return_value=MockedChannel('insecure sync test channel'))
@mock.patch("zepben.ewb.GrpcChannelBuilder._test_connection")
@mock.patch("grpc.aio.insecure_channel", return_value="insecure channel")
def test_for_address(mock_insecure_channel, mock_test_connection, mock_insecure_sync_channel):
    assert GrpcChannelBuilder().for_address("hostname", 1234).build() == "insecure channel"

    mock_insecure_sync_channel.assert_called_once_with("hostname:1234")
    mock_test_connection.assert_called_once_with(MockedChannel('insecure sync test channel'), debug=False, timeout_seconds=5)
    mock_insecure_channel.assert_called_once_with("hostname:1234", options=DEFAULT_GRPC_CHANNEL_OPTIONS)


@mock.patch("grpc.insecure_channel", return_value=MockedChannel('insecure sync test channel'))
@mock.patch("zepben.ewb.GrpcChannelBuilder._test_connection")
@mock.patch("grpc.aio.insecure_channel", return_value="insecure channel")
def test_options_passed_to_insecure_channel(mock_insecure_channel, *_):
    options = [("grpc.max_receive_message_length", 1), ("other_option", 1)]
    assert GrpcChannelBuilder().for_address("hostname", 1234).build(options=options) == "insecure channel"
    mock_insecure_channel.assert_called_once_with("hostname:1234", options=options)


@mock.patch("grpc.secure_channel", return_value=MockedChannel("secure sync test channel"))
@mock.patch("zepben.ewb.GrpcChannelBuilder._test_connection")
@mock.patch("grpc.ssl_channel_credentials", return_value="channel creds")
@mock.patch("grpc.aio.secure_channel", return_value="secure channel")
def test_options_passed_to_secure_channel(mocked_secure_channel, *_):
    options = [("grpc.max_receive_message_length", 1), ("other_option", 0)]
    assert GrpcChannelBuilder().for_address("hostname", 1234).make_secure_with_bytes().build(options=options) == "secure channel"
    mocked_secure_channel.assert_called_with("hostname:1234", "channel creds", options=options)


@mock.patch("grpc.insecure_channel", return_value=MockedChannel('insecure sync test channel'))
@mock.patch("zepben.ewb.GrpcChannelBuilder._test_connection")
@mock.patch("grpc.aio.insecure_channel", return_value="insecure channel")
def test_passed_options_override_defaults(mock_insecure_channel, *_):
    options = [("grpc.max_receive_message_length", 1), ("other_option", 0)]
    assert GrpcChannelBuilder().for_address("hostname", 1234).build(options=options) == "insecure channel"
    mock_insecure_channel.assert_called_once_with("hostname:1234", options=options)
    for option_key, option_value in mock_insecure_channel.call_args_list[0][1]["options"]:
        if option_key == "grpc.max_receive_message_length":
            assert option_value == 1
        if option_key == "grpc.max_send_message_length":
            assert option_value == _TWENTY_MEGABYTES
        if option_key == "other_option":
            assert option_value == 0


@mock.patch("grpc.secure_channel", return_value=MockedChannel("secure sync test channel"))
@mock.patch("zepben.ewb.GrpcChannelBuilder._test_connection")
@mock.patch("grpc.ssl_channel_credentials", return_value="channel creds")
@mock.patch("grpc.aio.secure_channel", return_value="secure channel")
def test_make_secure(mocked_secure_channel, mocked_ssl_channel_creds, mock_test_connection, mock_secure_sync_channel):
    assert GrpcChannelBuilder().for_address("hostname", 1234).make_secure_with_bytes(b"ca", b"cc", b"pk").build() == "secure channel"
    assert GrpcChannelBuilder().for_address("hostname", 1234).make_secure_with_bytes().build() == "secure channel"

    mocked_ssl_channel_creds.assert_has_calls([call(b"ca", b"pk", b"cc"), call(None, None, None)])
    mocked_secure_channel.assert_called_with("hostname:1234", "channel creds", options=DEFAULT_GRPC_CHANNEL_OPTIONS)
    mock_secure_sync_channel.assert_called_with("hostname:1234", "channel creds")
    mock_test_connection.assert_has_calls(
        [call(MockedChannel("secure sync test channel"), debug=False, timeout_seconds=5),
         call(MockedChannel("secure sync test channel"), debug=False, timeout_seconds=5)])


@mock.patch("builtins.open", side_effect=lambda filename, *args, **kwargs: MockReadable(str.encode(filename)))
@mock.patch("zepben.ewb.GrpcChannelBuilder.make_secure_with_bytes")
def test_make_secure_filename_version(mocked_mswb, mocked_open):
    GrpcChannelBuilder().make_secure("ca", "cc", "pk")
    GrpcChannelBuilder().make_secure()

    mocked_open.assert_has_calls([call("ca", "rb"), call("cc", "rb"), call("pk", "rb")], any_order=True)
    mocked_mswb.assert_has_calls([call(b"ca", b"cc", b"pk"), call(None, None, None)])


@mock.patch("grpc.secure_channel", return_value=MockedChannel("secure sync test channel"))
@mock.patch("zepben.ewb.GrpcChannelBuilder._test_connection")
@mock.patch("grpc.aio.secure_channel")
@mock.patch("grpc.composite_channel_credentials", return_value="composite creds")
@mock.patch("grpc.metadata_call_credentials", return_value="call creds")
@mock.patch("grpc.ssl_channel_credentials", return_value="ssl creds")
def test_with_token_fetcher(mocked_ssl_channel_creds, mocked_md_call_creds, mocked_comp_channel_creds, mocked_secure_channel, mock_test_connection,
                            mock_secure_sync_channel):
    GrpcChannelBuilder().for_address("hostname", 1234).make_secure().with_token_fetcher(
        ZepbenTokenFetcher("audience", "issuer_domain", "token_endpoint")).build()

    mocked_ssl_channel_creds.assert_called_once()
    mocked_md_call_creds.assert_called_once()
    mocked_comp_channel_creds.assert_called_once_with("ssl creds", "call creds")
    mocked_secure_channel.assert_called_once_with("hostname:1234", "composite creds", options=DEFAULT_GRPC_CHANNEL_OPTIONS)
    mock_secure_sync_channel.assert_called_once_with("hostname:1234", "composite creds")
    mock_test_connection.assert_called_once_with(MockedChannel('secure sync test channel'), timeout_seconds=5, debug=False)


def test_with_token_fetcher_before_make_secure():
    with pytest.raises(Exception, match="You must call make_secure before calling with_token_fetcher."):
        GrpcChannelBuilder().with_token_fetcher(ZepbenTokenFetcher("audience", "issuer_domain", "token_endpoint"))


def test_with_client_token_before_make_secure():
    with pytest.raises(Exception, match="You must call make_secure before calling with_client_token."):
        GrpcChannelBuilder().with_client_token("access_token")


@mock.patch("grpc._channel._UnaryUnaryMultiCallable.__call__",
            side_effect=[
                _InactiveRpcError(_RPCState(
                    [OperationType.send_message],
                    None,
                    None,
                    StatusCode.UNIMPLEMENTED,
                    "details"
                )),
                "empty response",
                Exception("Exception2")
            ])
def test_test_connection_returns_on_first_response(mock_checkConnection):
    channel = insecure_channel("unused")
    GrpcChannelBuilder()._test_connection(channel, False, timeout_seconds=5)

    mock_checkConnection.assert_has_calls([call(CheckConnectionRequest(), timeout=5, wait_for_ready=False),
                                           call(CheckConnectionRequest(), timeout=5, wait_for_ready=False)], any_order=False)
    assert mock_checkConnection.call_count == 2


@mock.patch("grpc._channel._UnaryUnaryMultiCallable.__call__",
            side_effect=[
                _InactiveRpcError(_RPCState(
                    [OperationType.send_message],
                    None,
                    None,
                    StatusCode.UNIMPLEMENTED,
                    "details"
                )),
                "metadata response",
                Exception("Exception2")
            ])
def test_test_connection_uses_timeout(mock_checkConnection):
    channel = insecure_channel("unused")
    GrpcChannelBuilder()._test_connection(channel, False, timeout_seconds=12345)

    mock_checkConnection.assert_has_calls([call(CheckConnectionRequest(), timeout=12345, wait_for_ready=False),
                                           call(CheckConnectionRequest(), timeout=12345, wait_for_ready=False)], any_order=False)
    assert mock_checkConnection.call_count == 2


@mock.patch("grpc._channel._UnaryUnaryMultiCallable.__call__", side_effect=[
    _InactiveRpcError(_RPCState(
        [OperationType.send_message],
        None,
        None,
        StatusCode.UNAVAILABLE,
        "details",
    ))
    ,
    "metadata response",
    Exception("Exception2")
])
def test_test_connection_continues_following_unavailable(mock_checkConnection):
    channel = insecure_channel("unused")
    GrpcChannelBuilder()._test_connection(channel, False, timeout_seconds=5)
    mock_checkConnection.assert_has_calls([call(CheckConnectionRequest(), timeout=5, wait_for_ready=False),
                                           call(CheckConnectionRequest(), timeout=5, wait_for_ready=False)], any_order=False)
    assert mock_checkConnection.call_count == 2


@mock.patch("grpc._channel._UnaryUnaryMultiCallable.__call__", side_effect=[
    _InactiveRpcError(_RPCState(
        [OperationType.send_message],
        None,
        None,
        StatusCode.DATA_LOSS,
        "details",
    )),
    _InactiveRpcError(_RPCState(
        [OperationType.send_message],
        None,
        None,
        StatusCode.DEADLINE_EXCEEDED,
        "details1",
    )),
    _InactiveRpcError(_RPCState(
        [OperationType.send_message],
        None,
        None,
        StatusCode.RESOURCE_EXHAUSTED,
        "details2",
    )),
    _InactiveRpcError(_RPCState(
        [OperationType.send_message],
        None,
        None,
        StatusCode.RESOURCE_EXHAUSTED,
        "details3",
    )),
    _InactiveRpcError(_RPCState(
        [OperationType.send_message],
        None,
        None,
        StatusCode.RESOURCE_EXHAUSTED,
        "details4",
    ))
])
def test_test_connection_raises_connection_exception(mock_checkConnection):
    channel = insecure_channel("unused")
    with pytest.raises(GrpcConnectionException, match="Couldn't establish gRPC connection to any service on myServer.myDomain:9999.\n"):
        GrpcChannelBuilder().for_address("myServer.myDomain", 9999)._test_connection(channel, False, timeout_seconds=5)
    mock_checkConnection.assert_has_calls(
        [call(CheckConnectionRequest(), timeout=5, wait_for_ready=False),
         call(CheckConnectionRequest(), timeout=5, wait_for_ready=False),
         call(CheckConnectionRequest(), timeout=5, wait_for_ready=False),
         call(CheckConnectionRequest(), timeout=5, wait_for_ready=False),
         call(CheckConnectionRequest(), timeout=5, wait_for_ready=False)]
    )
    assert mock_checkConnection.call_count == 5


@mock.patch("grpc._channel._UnaryUnaryMultiCallable.__call__", side_effect=[
    _InactiveRpcError(_RPCState(
        [OperationType.send_message],
        None,
        None,
        StatusCode.DATA_LOSS,
        "details1",
    )),
    _InactiveRpcError(_RPCState(
        [OperationType.send_message],
        None,
        None,
        StatusCode.DEADLINE_EXCEEDED,
        "details2",
    )),
    _InactiveRpcError(_RPCState(
        [OperationType.send_message],
        None,
        None,
        StatusCode.RESOURCE_EXHAUSTED,
        "details3",
    )),
    _InactiveRpcError(_RPCState(
        [OperationType.send_message],
        None,
        None,
        StatusCode.RESOURCE_EXHAUSTED,
        "details4",
    )),
    _InactiveRpcError(_RPCState(
        [OperationType.send_message],
        None,
        None,
        StatusCode.RESOURCE_EXHAUSTED,
        "details5",
    ))
])
def test_test_connection_raises_connection_exception_with_debug(mock_checkConnection):
    channel = insecure_channel("unused")
    with pytest.raises(GrpcConnectionException,
                       match='Couldn\'t establish gRPC connection to any service on myServer.myDomain:9999.\n'
                             'Received the following exception with NetworkConsumerClient:\n<_InactiveRpcError of RPC that terminated with:\n'
                             '\tstatus = StatusCode.DATA_LOSS\n\tdetails = "details1"\n\tdebug_error_string = "None"\n>\n'
                             'Received the following exception with DiagramConsumerClient:\n<_InactiveRpcError of RPC that terminated with:\n'
                             '\tstatus = StatusCode.DEADLINE_EXCEEDED\n\tdetails = "details2"\n\tdebug_error_string = "None"\n>\n'
                             'Received the following exception with CustomerConsumerClient:\n<_InactiveRpcError of RPC that terminated with:\n'
                             '\tstatus = StatusCode.RESOURCE_EXHAUSTED\n\tdetails = "details3"\n\tdebug_error_string = "None"\n>\n'
                             'Received the following exception with QueryNetworkStateClient:\n<_InactiveRpcError of RPC that terminated with:\n'
                             '\tstatus = StatusCode.RESOURCE_EXHAUSTED\n\tdetails = "details4"\n\tdebug_error_string = "None"\n>\n'
                             'Received the following exception with UpdateNetworkStateClient:\n<_InactiveRpcError of RPC that terminated with:\n'
                             '\tstatus = StatusCode.RESOURCE_EXHAUSTED\n\tdetails = "details5"\n\tdebug_error_string = "None"\n>\n'):
        GrpcChannelBuilder().for_address("myServer.myDomain", 9999)._test_connection(channel, True, timeout_seconds=5)
    mock_checkConnection.assert_has_calls(
        [call(CheckConnectionRequest(), timeout=5, wait_for_ready=False),
         call(CheckConnectionRequest(), timeout=5, wait_for_ready=False),
         call(CheckConnectionRequest(), timeout=5, wait_for_ready=False),
         call(CheckConnectionRequest(), timeout=5, wait_for_ready=False),
         call(CheckConnectionRequest(), timeout=5, wait_for_ready=False)]
    )
    assert mock_checkConnection.call_count == 5


def test_count_grpc_stubs():
    all_clients = all_subclasses(GrpcClient, 'zepben.ewb.streaming')
    expected_stubs = set()

    for name in map(lambda klass: klass.__name__, all_clients):
        expected_stubs.add(name.replace("Sync", ""))

    assert expected_stubs == set(GrpcChannelBuilder._stubs.keys())
