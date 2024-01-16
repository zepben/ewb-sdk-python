from unittest import mock
from unittest.mock import call

import pytest
from dataclassy import dataclass
from zepben.auth import ZepbenTokenFetcher

from zepben.evolve import GrpcChannelBuilder

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


@mock.patch("grpc.aio.insecure_channel", return_value="insecure channel")
def test_for_address(mock_insecure_channel):
    assert GrpcChannelBuilder().for_address("hostname", 1234).build() == "insecure channel"

    mock_insecure_channel.assert_called_once_with("hostname:1234", options=DEFAULT_GRPC_CHANNEL_OPTIONS)


@mock.patch("grpc.aio.insecure_channel", return_value="insecure channel")
def test_options_passed_to_insecure_channel(mock_insecure_channel, *_):
    options = [("grpc.max_receive_message_length", 1), ("other_option", 1)]
    assert GrpcChannelBuilder().for_address("hostname", 1234).build(options=options) == "insecure channel"
    mock_insecure_channel.assert_called_once_with("hostname:1234", options=options)


@mock.patch("grpc.ssl_channel_credentials", return_value="channel creds")
@mock.patch("grpc.aio.secure_channel", return_value="secure channel")
def test_options_passed_to_secure_channel(mocked_secure_channel, *_):
    options = [("grpc.max_receive_message_length", 1), ("other_option", 0)]
    assert GrpcChannelBuilder().for_address("hostname", 1234).make_secure_with_bytes().build(options=options) == "secure channel"
    mocked_secure_channel.assert_called_with("hostname:1234", "channel creds", options=options)


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


@mock.patch("grpc.ssl_channel_credentials", return_value="channel creds")
@mock.patch("grpc.aio.secure_channel", return_value="secure channel")
def test_make_secure(mocked_secure_channel, mocked_ssl_channel_creds):
    assert GrpcChannelBuilder().for_address("hostname", 1234).make_secure_with_bytes(b"ca", b"cc", b"pk").build() == "secure channel"
    assert GrpcChannelBuilder().for_address("hostname", 1234).make_secure_with_bytes().build() == "secure channel"

    mocked_ssl_channel_creds.assert_has_calls([call(b"ca", b"pk", b"cc"), call(None, None, None)])
    mocked_secure_channel.assert_called_with("hostname:1234", "channel creds", options=DEFAULT_GRPC_CHANNEL_OPTIONS)


@mock.patch("builtins.open", side_effect=lambda filename, *args, **kwargs: MockReadable(str.encode(filename)))
@mock.patch("zepben.evolve.GrpcChannelBuilder.make_secure_with_bytes")
def test_make_secure_filename_version(mocked_mswb, mocked_open):
    GrpcChannelBuilder().make_secure("ca", "cc", "pk")
    GrpcChannelBuilder().make_secure()

    mocked_open.assert_has_calls([call("ca", "rb"), call("cc", "rb"), call("pk", "rb")], any_order=True)
    mocked_mswb.assert_has_calls([call(b"ca", b"cc", b"pk"), call(None, None, None)])


@mock.patch("grpc.aio.secure_channel")
@mock.patch("grpc.composite_channel_credentials", return_value="composite creds")
@mock.patch("grpc.metadata_call_credentials", return_value="call creds")
@mock.patch("grpc.ssl_channel_credentials", return_value="ssl creds")
def test_with_token_fetcher(mocked_ssl_channel_creds, mocked_md_call_creds, mocked_comp_channel_creds, mocked_secure_channel):
    GrpcChannelBuilder().for_address("hostname", 1234).make_secure().with_token_fetcher(ZepbenTokenFetcher("audience", "issuer_domain")).build()

    mocked_ssl_channel_creds.assert_called_once()
    mocked_md_call_creds.assert_called_once()
    mocked_comp_channel_creds.assert_called_once_with("ssl creds", "call creds")
    mocked_secure_channel.assert_called_once_with("hostname:1234", "composite creds", options=DEFAULT_GRPC_CHANNEL_OPTIONS)


def test_with_token_fetcher_before_make_secure():
    with pytest.raises(Exception, match="You must call make_secure before calling with_token_fetcher."):
        GrpcChannelBuilder().with_token_fetcher(ZepbenTokenFetcher("audience", "issuer_domain"))
