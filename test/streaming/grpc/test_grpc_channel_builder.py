from unittest import mock
from unittest.mock import call

import pytest
from dataclassy import dataclass
from zepben.auth.client import ZepbenTokenFetcher

from zepben.evolve import GrpcChannelBuilder


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

    mock_insecure_channel.assert_called_once_with("hostname:1234")


@mock.patch("grpc.ssl_channel_credentials", return_value="channel creds")
@mock.patch("grpc.aio.secure_channel", return_value="secure channel")
def test_make_secure(mocked_secure_channel, mocked_ssl_channel_creds):
    assert GrpcChannelBuilder().for_address("hostname", 1234).make_secure_with_bytes(b"ca", b"cc", b"pk").build() == "secure channel"
    assert GrpcChannelBuilder().for_address("hostname", 1234).make_secure_with_bytes().build() == "secure channel"

    mocked_ssl_channel_creds.assert_has_calls([call(b"ca", b"pk", b"cc"), call(None, None, None)])
    mocked_secure_channel.assert_called_with("hostname:1234", "channel creds")


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
    mocked_secure_channel.assert_called_once_with("hostname:1234", "composite creds")


def test_with_token_fetcher_before_make_secure():
    with pytest.raises(Exception, match="You must call make_secure before calling with_token_fetcher."):
        GrpcChannelBuilder().with_token_fetcher(ZepbenTokenFetcher("audience", "issuer_domain"))
