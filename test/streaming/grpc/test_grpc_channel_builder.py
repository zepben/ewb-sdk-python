from unittest import mock
from unittest.mock import call

import pytest
from dataclassy import dataclass
from grpc._channel import _InactiveRpcError, _RPCState
from grpc._cython.cygrpc import OperationType
from grpc import StatusCode, insecure_channel
from zepben.auth import ZepbenTokenFetcher
from zepben.protobuf.metadata.metadata_requests_pb2 import GetMetadataRequest

from zepben.evolve import GrpcChannelBuilder, GrpcConnectionException


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


@mock.patch("zepben.evolve.GrpcChannelBuilder._test_connection")
@mock.patch("grpc.aio.insecure_channel", return_value="insecure channel")
def test_skip_connection_test(mock_insecure_channel, mock_test_connection):
    assert GrpcChannelBuilder().build(skip_connection_test=True) == "insecure channel"

    mock_insecure_channel.assert_called_once_with('localhost:50051')
    mock_test_connection.assert_not_called()


@mock.patch("grpc.insecure_channel", return_value=MockedChannel('insecure sync test channel'))
@mock.patch("zepben.evolve.GrpcChannelBuilder._test_connection")
@mock.patch("grpc.aio.insecure_channel", return_value="insecure channel")
def test_debug_connection_test(mock_insecure_channel, mock_test_connection, mock_insecure_sync_channel):
    assert GrpcChannelBuilder().build(debug=True) == "insecure channel"

    mock_insecure_sync_channel.assert_called_once_with("localhost:50051")
    mock_test_connection.assert_called_once_with(MockedChannel('insecure sync test channel'), debug=True)
    mock_insecure_channel.assert_called_once_with('localhost:50051')


@mock.patch("grpc.insecure_channel", return_value=MockedChannel('insecure sync test channel'))
@mock.patch("zepben.evolve.GrpcChannelBuilder._test_connection")
@mock.patch("grpc.aio.insecure_channel", return_value="insecure channel")
def test_for_address(mock_insecure_channel, mock_test_connection, mock_insecure_sync_channel):
    assert GrpcChannelBuilder().for_address("hostname", 1234).build() == "insecure channel"

    mock_insecure_sync_channel.assert_called_once_with("hostname:1234")
    mock_test_connection.assert_called_once_with(MockedChannel('insecure sync test channel'), debug=False)
    mock_insecure_channel.assert_called_once_with("hostname:1234")


@mock.patch("grpc.secure_channel", return_value=MockedChannel("secure sync test channel"))
@mock.patch("zepben.evolve.GrpcChannelBuilder._test_connection")
@mock.patch("grpc.ssl_channel_credentials", return_value="channel creds")
@mock.patch("grpc.aio.secure_channel", return_value="secure channel")
def test_make_secure(mocked_secure_channel, mocked_ssl_channel_creds, mock_test_connection, mock_secure_sync_channel):
    assert GrpcChannelBuilder().for_address("hostname", 1234).make_secure_with_bytes(b"ca", b"cc", b"pk").build() == "secure channel"
    assert GrpcChannelBuilder().for_address("hostname", 1234).make_secure_with_bytes().build() == "secure channel"

    mocked_ssl_channel_creds.assert_has_calls([call(b"ca", b"pk", b"cc"), call(None, None, None)])
    mocked_secure_channel.assert_called_with("hostname:1234", "channel creds")
    mock_secure_sync_channel.assert_called_with("hostname:1234", "channel creds")
    mock_test_connection.assert_has_calls(
        [call(MockedChannel("secure sync test channel"), debug=False), call(MockedChannel("secure sync test channel"), debug=False)])


@mock.patch("builtins.open", side_effect=lambda filename, *args, **kwargs: MockReadable(str.encode(filename)))
@mock.patch("zepben.evolve.GrpcChannelBuilder.make_secure_with_bytes")
def test_make_secure_filename_version(mocked_mswb, mocked_open):
    GrpcChannelBuilder().make_secure("ca", "cc", "pk")
    GrpcChannelBuilder().make_secure()

    mocked_open.assert_has_calls([call("ca", "rb"), call("cc", "rb"), call("pk", "rb")], any_order=True)
    mocked_mswb.assert_has_calls([call(b"ca", b"cc", b"pk"), call(None, None, None)])


@mock.patch("grpc.secure_channel", return_value=MockedChannel("secure sync test channel"))
@mock.patch("zepben.evolve.GrpcChannelBuilder._test_connection")
@mock.patch("grpc.aio.secure_channel")
@mock.patch("grpc.composite_channel_credentials", return_value="composite creds")
@mock.patch("grpc.metadata_call_credentials", return_value="call creds")
@mock.patch("grpc.ssl_channel_credentials", return_value="ssl creds")
def test_with_token_fetcher(mocked_ssl_channel_creds, mocked_md_call_creds, mocked_comp_channel_creds, mocked_secure_channel, mock_test_connection,
                            mock_secure_sync_channel):
    GrpcChannelBuilder().for_address("hostname", 1234).make_secure().with_token_fetcher(
        ZepbenTokenFetcher("audience", "issuer_domain")).build()

    mocked_ssl_channel_creds.assert_called_once()
    mocked_md_call_creds.assert_called_once()
    mocked_comp_channel_creds.assert_called_once_with("ssl creds", "call creds")
    mocked_secure_channel.assert_called_once_with("hostname:1234", "composite creds")
    mock_secure_sync_channel.assert_called_once_with("hostname:1234", "composite creds")
    mock_test_connection.assert_called_once_with(MockedChannel('secure sync test channel'), debug=False)


def test_with_token_fetcher_before_make_secure():
    with pytest.raises(Exception, match="You must call make_secure before calling with_token_fetcher."):
        GrpcChannelBuilder().with_token_fetcher(ZepbenTokenFetcher("audience", "issuer_domain"))


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
def test_test_connection_returns_on_first_response(mock_getMetadata):
    channel = insecure_channel("unused")
    GrpcChannelBuilder()._test_connection(channel, False)

    mock_getMetadata.assert_has_calls([call(GetMetadataRequest(), wait_for_ready=False),
                                       call(GetMetadataRequest(), wait_for_ready=False)], any_order=False)
    assert mock_getMetadata.call_count == 2


@mock.patch("grpc._channel._UnaryUnaryMultiCallable.__call__", side_effect=[
    _InactiveRpcError(_RPCState(
        [OperationType.send_message],
        None,
        None,
        StatusCode.UNAVAILABLE,
        "details",
    ))
    ,
    Exception("Exception1"),
    Exception("Exception2")
])
def test_test_connection_raises_on_first_unavailable(mock_getMetadata):
    channel = insecure_channel("unused")
    with pytest.raises(_InactiveRpcError, match='<_InactiveRpcError of RPC that terminated with:\n\tstatus = StatusCode.UNAVAILABLE\n\tdetails = '
                                                '"details"\n\tdebug_error_string = "None"\n>'):
        GrpcChannelBuilder()._test_connection(channel, False)
    mock_getMetadata.assert_called_once()


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
    ))
])
def test_test_connection_raises_connection_exception(mock_getMetadata):
    channel = insecure_channel("unused")
    with pytest.raises(GrpcConnectionException, match="Couldn't establish gRPC connection to any service on myServer.myDomain:9999.\n"):
        GrpcChannelBuilder().for_address("myServer.myDomain", 9999)._test_connection(channel, False)
    mock_getMetadata.assert_has_calls(
        [call(GetMetadataRequest(), wait_for_ready=False),
         call(GetMetadataRequest(), wait_for_ready=False),
         call(GetMetadataRequest(), wait_for_ready=False)]
    )
    assert mock_getMetadata.call_count == 3


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
    ))
])
def test_test_connection_raises_connection_exception_with_debug(mock_getMetadata):
    channel = insecure_channel("unused")
    with pytest.raises(GrpcConnectionException,
                       match='Couldn\'t establish gRPC connection to any service on myServer.myDomain:9999.\n'
                             'Received the following exception with NetworkConsumerStub:\n<_InactiveRpcError of RPC that terminated with:\n'
                             '\tstatus = StatusCode.DATA_LOSS\n\tdetails = "details1"\n\tdebug_error_string = "None"\n>\n'
                             'Received the following exception with DiagramConsumerStub:\n<_InactiveRpcError of RPC that terminated with:\n'
                             '\tstatus = StatusCode.DEADLINE_EXCEEDED\n\tdetails = "details2"\n\tdebug_error_string = "None"\n>\n'
                             'Received the following exception with CustomerConsumerStub:\n<_InactiveRpcError of RPC that terminated with:\n'
                             '\tstatus = StatusCode.RESOURCE_EXHAUSTED\n\tdetails = "details3"\n\tdebug_error_string = "None"\n>\n'):
        GrpcChannelBuilder().for_address("myServer.myDomain", 9999)._test_connection(channel, True)
    mock_getMetadata.assert_has_calls(
        [call(GetMetadataRequest(), wait_for_ready=False),
         call(GetMetadataRequest(), wait_for_ready=False),
         call(GetMetadataRequest(), wait_for_ready=False)]
    )
    assert mock_getMetadata.call_count == 3
