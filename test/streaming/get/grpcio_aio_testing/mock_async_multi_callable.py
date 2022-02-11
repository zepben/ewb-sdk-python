#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional, Any, TypeVar

import grpc
from grpc.aio import UnaryUnaryCall, StreamStreamCall, StreamUnaryCall, UnaryStreamCall
from grpc_testing import _common
from grpc_testing._channel import _invocation

from test.streaming.get.grpcio_aio_testing.mock_async_calls import UnaryResponse, ResponseIteratorCall

MetadataType = TypeVar("MetadataType")
RequestIterableType = TypeVar("RequestIterableType")


# All per-call credentials parameters are unused by this test infrastructure.
# pylint: disable=unused-argument
class UnaryUnary(grpc.aio.UnaryUnaryMultiCallable):

    def __init__(self, method_full_rpc_name, channel_handler):
        self._method_full_rpc_name = method_full_rpc_name
        self._channel_handler = channel_handler

    def __call__(
        self,
        request: Any,
        *,
        timeout: Optional[float] = None,
        metadata: Optional[MetadataType] = None,
        credentials: Optional[grpc.CallCredentials] = None,
        wait_for_ready: Optional[bool] = None,
        compression: Optional[grpc.Compression] = None
    ) -> UnaryUnaryCall:
        rpc_handler = self._channel_handler.invoke_rpc(
            self._method_full_rpc_name, _common.fuss_with_metadata(metadata),
            [request], True, timeout)
        return UnaryResponse(rpc_handler)


class UnaryStream(grpc.aio.UnaryStreamMultiCallable):

    def __init__(self, method_full_rpc_name, channel_handler):
        self._method_full_rpc_name = method_full_rpc_name
        self._channel_handler = channel_handler

    def __call__(
        self,
        request_iterator: Optional[RequestIterableType] = None,
        timeout: Optional[float] = None,
        metadata: Optional[MetadataType] = None,
        credentials: Optional[grpc.CallCredentials] = None,
        wait_for_ready: Optional[bool] = None,
        compression: Optional[grpc.Compression] = None
    ) -> UnaryStreamCall:
        rpc_handler = self._channel_handler.invoke_rpc(
            self._method_full_rpc_name, _common.fuss_with_metadata(metadata),
            [request_iterator], True, timeout)
        return ResponseIteratorCall(rpc_handler)


class StreamUnary(grpc.aio.StreamUnaryMultiCallable):

    def __init__(self, method_full_rpc_name, channel_handler):
        self._method_full_rpc_name = method_full_rpc_name
        self._channel_handler = channel_handler

    def __call__(
        self,
        request_iterator: Optional[RequestIterableType] = None,
        timeout: Optional[float] = None,
        metadata: Optional[MetadataType] = None,
        credentials: Optional[grpc.CallCredentials] = None,
        wait_for_ready: Optional[bool] = None,
        compression: Optional[grpc.Compression] = None
    ) -> StreamUnaryCall:
        rpc_handler = self._channel_handler.invoke_rpc(
            self._method_full_rpc_name, _common.fuss_with_metadata(metadata),
            [], False, timeout)
        _invocation.consume_requests(request_iterator, rpc_handler)
        return UnaryResponse(rpc_handler)


class StreamStream(grpc.aio.StreamStreamMultiCallable):

    def __init__(self, method_full_rpc_name, channel_handler):
        self._method_full_rpc_name = method_full_rpc_name
        self._channel_handler = channel_handler

    def __call__(
        self,
        request_iterator: Optional[RequestIterableType] = None,
        timeout: Optional[float] = None,
        metadata: Optional[MetadataType] = None,
        credentials: Optional[grpc.CallCredentials] = None,
        wait_for_ready: Optional[bool] = None,
        compression: Optional[grpc.Compression] = None
    ) -> StreamStreamCall:
        rpc_handler = self._channel_handler.invoke_rpc(
            self._method_full_rpc_name, _common.fuss_with_metadata(metadata),
            [], False, timeout)
        _invocation.consume_requests(request_iterator, rpc_handler)
        return ResponseIteratorCall(rpc_handler)
