#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import Mock
from unittest import mock

import pytest

from zepben.evolve import connect_insecure, connect_tls, connect_with_secret, connect_with_password

base_gcb = Mock()
addressed_gcb = Mock()
secure_gcb = Mock()
authenticated_gcb = Mock()
insecure_channel = Mock()
secure_channel = Mock()
authenticated_channel = Mock()
token_fetcher = Mock()
token_fetcher.token_request_data = {}

base_gcb.for_address = Mock(return_value=addressed_gcb)
addressed_gcb.make_secure = Mock(return_value=secure_gcb)
secure_gcb.with_token_fetcher = Mock(return_value=authenticated_gcb)
addressed_gcb.build = Mock(return_value=insecure_channel)
secure_gcb.build = Mock(return_value=secure_channel)
authenticated_gcb.build = Mock(return_value=authenticated_channel)


@pytest.fixture(autouse=True)
def before_each():
    base_gcb.reset_mock()
    addressed_gcb.reset_mock()
    secure_gcb.reset_mock()
    authenticated_gcb.reset_mock()
    insecure_channel.reset_mock()
    secure_channel.reset_mock()
    authenticated_channel.reset_mock()
    token_fetcher.reset_mock()
    token_fetcher.reset_mock()
    token_fetcher.token_request_data.clear()


@mock.patch("zepben.evolve.streaming.grpc.connect.GrpcChannelBuilder", return_value=base_gcb)
def test_connect_insecure(_):
    assert connect_insecure("hostname", 1234) is insecure_channel

    base_gcb.for_address.assert_called_once_with("hostname", 1234)


@mock.patch("zepben.evolve.streaming.grpc.connect.GrpcChannelBuilder", return_value=base_gcb)
def test_connect_tls(_):
    assert connect_tls("hostname", 1234, "ca.cert") is secure_channel

    base_gcb.for_address.assert_called_once_with("hostname", 1234)
    addressed_gcb.make_secure.assert_called_once_with(root_certificates="ca.cert")


@mock.patch("zepben.evolve.streaming.grpc.connect.GrpcChannelBuilder", return_value=base_gcb)
@mock.patch("zepben.evolve.streaming.grpc.connect.create_token_fetcher", return_value=token_fetcher)
def test_connect_with_secret(mocked_create_token_fetcher, _):
    assert connect_with_secret("client_id", "client_secret", "host", 1234, "conf_address", False, "auth_ca.cert", "ca.cert") is authenticated_channel
    assert token_fetcher.token_request_data == {
        "client_id": "client_id",
        "client_secret": "client_secret",
        "grant_type": "client_credentials"
    }

    mocked_create_token_fetcher.assert_called_once_with(conf_address="conf_address", verify_conf=False, verify_auth="auth_ca.cert")


@mock.patch("zepben.evolve.streaming.grpc.connect.connect_tls", return_value=secure_channel)
@mock.patch("zepben.evolve.streaming.grpc.connect.create_token_fetcher", return_value=None)
def test_connect_with_secret_connects_with_tls_if_no_auth(mocked_create_token_fetcher, _):
    assert connect_with_secret("client_id", "client_secret", "host", 1234, "conf_address", False, "auth_ca.cert", "ca.cert") is secure_channel

    mocked_create_token_fetcher.assert_called_once_with(conf_address="conf_address", verify_conf=False, verify_auth="auth_ca.cert")


@mock.patch("zepben.evolve.streaming.grpc.connect.GrpcChannelBuilder", return_value=base_gcb)
@mock.patch("zepben.evolve.streaming.grpc.connect.create_token_fetcher", return_value=token_fetcher)
def test_connect_with_secret_defaults(mocked_create_token_fetcher, _):
    assert connect_with_secret("client_id", "client_secret", host="host", rpc_port=1234) is authenticated_channel
    assert token_fetcher.token_request_data == {
        "client_id": "client_id",
        "client_secret": "client_secret",
        "grant_type": "client_credentials"
    }

    mocked_create_token_fetcher.assert_called_once_with(conf_address="https://host/ewb/auth", verify_conf=True, verify_auth=True)


@mock.patch("zepben.evolve.streaming.grpc.connect.GrpcChannelBuilder", return_value=base_gcb)
@mock.patch("zepben.evolve.streaming.grpc.connect.create_token_fetcher", return_value=token_fetcher)
def test_connect_with_password(mocked_create_token_fetcher, _):
    assert connect_with_password("client_id", "username", "password", "host", 1234, "conf_address", False, "auth_ca.cert", "ca.cert") is authenticated_channel
    assert token_fetcher.token_request_data == {
        "client_id": "client_id",
        "username": "username",
        "password": "password",
        "grant_type": "password",
        "scope": "offline_access"
    }

    mocked_create_token_fetcher.assert_called_once_with(conf_address="conf_address", verify_conf=False, verify_auth="auth_ca.cert")


@mock.patch("zepben.evolve.streaming.grpc.connect.connect_tls", return_value=secure_channel)
@mock.patch("zepben.evolve.streaming.grpc.connect.create_token_fetcher", return_value=None)
def test_connect_with_password_connects_with_tls_if_no_auth(mocked_create_token_fetcher, _):
    assert connect_with_password("client_id", "username", "password", "host", 1234, "conf_address", False, "auth_ca.cert", "ca.cert") is secure_channel

    mocked_create_token_fetcher.assert_called_once_with(conf_address="conf_address", verify_conf=False, verify_auth="auth_ca.cert")


@mock.patch("zepben.evolve.streaming.grpc.connect.GrpcChannelBuilder", return_value=base_gcb)
@mock.patch("zepben.evolve.streaming.grpc.connect.create_token_fetcher", return_value=token_fetcher)
def test_connect_with_password_defaults(mocked_create_token_fetcher, _):
    assert connect_with_password("client_id", "username", "password", "host", 1234) is authenticated_channel
    assert token_fetcher.token_request_data == {
        "client_id": "client_id",
        "username": "username",
        "password": "password",
        "grant_type": "password",
        "scope": "offline_access"
    }

    mocked_create_token_fetcher.assert_called_once_with(conf_address="https://host/ewb/auth", verify_conf=True, verify_auth=True)
