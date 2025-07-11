#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import random
import re
import string
from unittest import mock
from unittest.mock import ANY

import pytest
from zepben.ewb.auth import ZepbenTokenFetcher, AuthException, create_token_fetcher, AuthMethod
from zepben.ewb.auth.client.zepben_token_fetcher import _fetch_token_generator

TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZha2VraWQifQ.eyJpc3MiOiJodHRwczovL2lzc3Vlci8iLCJzdWIiOiJmYWtlIiwiYXVkIjoiaHR0cHM6Ly9mYWtlLWF1ZC8iLCJpYXQiOjE1OTE4MzQxNzksImV4cCI6OTU5MTkyMDU3OSwiYXpwIjoid2U5ZDNSME5jTUNWckpDZ2ROSWVmWWx6aHo2VE9SaGciLCJzY29wZSI6IndyaXRlOm5ldHdvcmsgcmVhZDpuZXR3b3JrIHdyaXRlOm1ldHJpY3MgcmVhZDpld2IiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6WyJ3cml0ZTpuZXR3b3JrIiwicmVhZDpuZXR3b3JrIiwid3JpdGU6bWV0cmljcyIsInJlYWQ6ZXdiIl19.ay_YTwRsfcNzVdmQ4EgmuNMMypfZIIc8K9dCCtLqUmUJDtE7NUuKaVAmGDdmW1J-ngm0UsH4k6B5QpPIJnLIROpdDf7aRzdE9hNFuSHR3arpyCzmO2-TiFDZLFXQjHf0Q-BaxGoXLQBupGYuQaG_3flaLPB3hPV0nqPoBTIoJgG8n2w0Uo2tePe_y2Blqco1sK2wElwyMlYc-UuTyFSvwKlpSXYmO4ppVmbAa9lS2ley6lcv2TwXLCk0KfIIH2E5OBvJHevZqYEzFBAeLCnahKoWxexsVvEfZr40Nhc6oPRT5yJfHRBnCrDnO1fE96rqguQpsDG-HWCtd2GkpnAXNg"

mock_audience = ''.join(random.choices(string.ascii_lowercase, k=10))
mock_token_endpoint = ''.join(random.choices(string.ascii_lowercase, k=10))
mock_access_token = ''.join(random.choices(string.ascii_lowercase, k=10))
mock_refresh_token = ''.join(random.choices(string.ascii_lowercase, k=10))
mock_issuer = ''.join(random.choices(string.ascii_lowercase, k=10))
mock_auth_method = random.choice(list(AuthMethod))
mock_verify_certificate = bool(random.getrandbits(1))


class MockResponse:
    def __init__(self, json_data, status_code, reason="", text=""):
        self.json_data = json_data
        self.status_code = status_code
        self.ok = status_code < 400
        self.reason = reason
        self.text = text

    def json(self):
        if not self.json_data:
            raise ValueError()
        return self.json_data


@mock.patch('zepben.ewb.auth.common.auth_provider_config.requests.get', side_effect=lambda *args, **kwargs: MockResponse(
    {"authType": "OAUTH", "audience": mock_audience, "issuer": mock_issuer}, 200))
def test_create_token_fetcher_success(mock_get):
    token_fetcher = create_token_fetcher(mock_issuer)
    assert token_fetcher is not None
    assert token_fetcher.audience == mock_audience

    mock_get.assert_called_with(
        mock_issuer + "/.well-known/openid-configuration"
    )


@mock.patch('zepben.ewb.auth.common.auth_provider_config.requests.get', side_effect=lambda *args, **kwargs: MockResponse(
    {"authType": "NONE", "audience": "", "issuer": ""}, 200))
def test_create_token_fetcher_no_auth(mock_get):
    with pytest.raises(AuthException, match=re.escape("authMethod 'NONE' is not supported for token fetching!")) as exc_info:
        create_token_fetcher("https://testaddress:443/ewb/auth")

    assert exc_info.value.status_code == 1

    mock_get.assert_called_with(
        "https://testaddress:443/ewb/auth",
        verify=True
    )


@mock.patch('zepben.ewb.auth.client.zepben_token_fetcher.requests.get', side_effect=lambda *args, **kwargs: MockResponse(None, 404))
def test_create_token_fetcher_bad_response(mock_get):
    with pytest.raises(AuthException, match=re.escape("https://testaddress:443/ewb/auth responded with: ")) as exc_info:
        create_token_fetcher("https://testaddress:443/ewb/auth")

    assert exc_info.value.status_code == 404

    mock_get.assert_called_once_with(
        "https://testaddress:443/ewb/auth",
        verify=True
    )


@mock.patch('zepben.ewb.auth.client.zepben_token_fetcher.requests.get',
            side_effect=lambda *args, **kwargs: MockResponse(None, 200, reason='test reason', text='test text'))
def test_create_token_fetcher_missing_json(mock_get):
    with pytest.raises(AuthException, match=f"Expected JSON response from https://testaddress:443/ewb/auth, but got: test text.") as exc_info:
        create_token_fetcher("https://testaddress:443/ewb/auth")

    assert exc_info.value.status_code == 200

    mock_get.assert_called_once_with(
        "https://testaddress:443/ewb/auth",
        verify=True
    )


class TestZepbenTokenFetcher:

    @mock.patch('zepben.ewb.auth.client.zepben_token_fetcher.requests.post', side_effect=lambda *args, **kwargs: MockResponse(
        {"access_token": TOKEN, "refresh_token": mock_refresh_token, "token_type": "Bearer"}, 200))
    def test_fetch_token_successful(self, mock_post):
        token_fetcher = ZepbenTokenFetcher(
            audience=mock_audience,
            auth_method=mock_auth_method,
            token_endpoint=mock_token_endpoint,
            verify=mock_verify_certificate,
        )

        mock_post.assert_not_called()  # POST request is not made before get_token() is called

        assert f"Bearer {TOKEN}" == token_fetcher.fetch_token()  # Token from response payload is returned

        mock_post.assert_called_once_with(
            url=mock_token_endpoint,
            headers=ANY,
            data=token_fetcher.token_request_data,
            verify=mock_verify_certificate
        )  # Appropriate-looking password grant request was made to the issuer

    @mock.patch('zepben.ewb.auth.client.zepben_token_fetcher.requests.post', side_effect=lambda *args, **kwargs: MockResponse(
        {"access_token": TOKEN, "refresh_token": mock_refresh_token, "token_type": "Bearer"}, 200))
    def test_fetch_token_azure_successful(self, mock_post):
        token_fetcher = ZepbenTokenFetcher(
            audience=mock_audience,
            token_endpoint=mock_token_endpoint,
            auth_method=AuthMethod.ENTRAID,
            verify=mock_verify_certificate,
            _request_token=_fetch_token_generator(True, False)
        )

        mock_post.assert_not_called()  # POST request is not made before get_token() is called

        assert f"Bearer {TOKEN}" == token_fetcher.fetch_token()  # Token from response payload is returned

        mock_post.assert_called_once_with(
            url=mock_token_endpoint,
            headers=ANY,
            data=token_fetcher.token_request_data,
            verify=mock_verify_certificate
        )  # Appropriate-looking password grant request was made to the issuer

    @mock.patch('zepben.ewb.auth.client.zepben_token_fetcher.requests.get', side_effect=lambda *args, **kwargs: MockResponse(
        {"access_token": TOKEN, "refresh_token": mock_refresh_token, "token_type": "Bearer"}, 200))
    def test_fetch_token_managed_identity_successful(self, mock_post):
        token_fetcher = ZepbenTokenFetcher(
            audience=mock_audience,
            token_endpoint=mock_token_endpoint,
            auth_method=AuthMethod.ENTRAID,
            verify=mock_verify_certificate,
            _request_token=_fetch_token_generator(True, True, mock_token_endpoint)
        )

        mock_post.assert_not_called()  # POST request is not made before get_token() is called

        assert f"Bearer {TOKEN}" == token_fetcher.fetch_token()  # Token from response payload is returned

        mock_post.assert_called_once_with(
            mock_token_endpoint,
            headers={'Metadata': 'true'},
            verify=mock_verify_certificate
        )  # Appropriate-looking identity request was made to the issuer

    @mock.patch('zepben.ewb.auth.client.zepben_token_fetcher.requests.post', side_effect=lambda *args, **kwargs: MockResponse(None, 404, "test reason", "test text"))
    def test_fetch_token_throws_exception_on_bad_response(self, mock_post):
        token_fetcher = ZepbenTokenFetcher(
            audience=mock_audience,
            token_endpoint="some_url",
            auth_method=mock_auth_method,
            verify=mock_verify_certificate
        )

        mock_post.assert_not_called()  # POST request is not made before get_token() is called

        with pytest.raises(AuthException, match=f"Token fetch failed, Error was: test reason test text") as exc_info:
            token_fetcher.fetch_token()

        assert exc_info.value.status_code == 404

        mock_post.assert_called_once_with(
            url="some_url",
            headers=ANY,
            data=token_fetcher.token_request_data,
            verify=mock_verify_certificate
        )

    @mock.patch('zepben.ewb.auth.client.zepben_token_fetcher.requests.post', side_effect=lambda *args, **kwargs: MockResponse(None, 200, "test reason", "test text"))
    def test_fetch_token_throws_exception_on_missing_json(self, mock_post):
        token_fetcher = ZepbenTokenFetcher(
            audience=mock_audience,
            token_endpoint=mock_token_endpoint,
            auth_method=mock_auth_method,
            verify=mock_verify_certificate
        )

        mock_post.assert_not_called()  # POST request is not made before get_token() is called

        with pytest.raises(AuthException, match=f'Response did not contain expected JSON - response was: test text'):
            token_fetcher.fetch_token()

        mock_post.assert_called_once_with(
            url=mock_token_endpoint,
            headers=ANY,
            data=token_fetcher.token_request_data,
            verify=mock_verify_certificate
        )

    @mock.patch('zepben.ewb.auth.client.zepben_token_fetcher.requests.post',
                side_effect=lambda *args, **kwargs: MockResponse({'error': 'fail', 'error_description': 'test error description'}, 200))
    def test_fetch_token_throws_exception_on_error_response(self, mock_post):
        token_fetcher = ZepbenTokenFetcher(
            audience=mock_audience,
            token_endpoint=mock_token_endpoint,
            auth_method=mock_auth_method,
            verify=mock_verify_certificate
        )

        mock_post.assert_not_called()  # POST request is not made before get_token() is called

        with pytest.raises(AuthException, match=f'fail - test error description'):
            token_fetcher.fetch_token()

        mock_post.assert_called_once_with(
            url=mock_token_endpoint,
            headers=ANY,
            data=token_fetcher.token_request_data,
            verify=mock_verify_certificate
        )

    @mock.patch('zepben.ewb.auth.client.zepben_token_fetcher.requests.post',
                side_effect=lambda *args, **kwargs: MockResponse({'test': 'fail'}, 200))
    def test_fetch_token_throws_exception_on_missing_access_token(self, mock_post):
        token_fetcher = ZepbenTokenFetcher(
            audience=mock_audience,
            token_endpoint=mock_token_endpoint,
            auth_method=mock_auth_method,
            verify=mock_verify_certificate
        )

        mock_post.assert_not_called()  # POST request is not made before get_token() is called

        with pytest.raises(AuthException, match="Access Token absent in token response - Response was: {'test': 'fail'}"):
            token_fetcher.fetch_token()

        mock_post.assert_called_once_with(
            url=mock_token_endpoint,
            headers=ANY,
            data=token_fetcher.token_request_data,
            verify=mock_verify_certificate
        )

    @mock.patch('zepben.ewb.auth.client.zepben_token_fetcher.requests.post', side_effect=lambda *args, **kwargs: MockResponse(
        {"access_token": TOKEN, "refresh_token": mock_refresh_token, "token_type": "Bearer"}, 200))
    def test_fetch_token_successful_using_refresh(self, mock_post):
        token_fetcher = ZepbenTokenFetcher(
            audience=mock_audience,
            token_endpoint=mock_token_endpoint,
            auth_method=mock_auth_method,
            verify=mock_verify_certificate
        )

        token_fetcher.refresh_request_data['refresh_token'] = mock_refresh_token
        mock_post.assert_not_called()  # POST request is not made before get_token() is called
        token_fetcher._refresh_token = mock_refresh_token
        assert f"Bearer {TOKEN}" == token_fetcher.fetch_token()

        mock_post.assert_called_once_with(
            url=mock_token_endpoint,
            headers=ANY,
            data=token_fetcher.refresh_request_data,
            verify=mock_verify_certificate
        )
