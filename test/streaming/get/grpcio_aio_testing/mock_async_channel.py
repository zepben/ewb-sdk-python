#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Copyright 2017 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#  Modifications Copyright Zeppelin Bend Pty Ltd as stated above
import abc
import asyncio

import grpc
import six
from grpc_testing._channel import _channel_rpc, _channel_state
from grpc_testing._channel._channel_state import State

from streaming.get.grpcio_aio_testing.mock_async_multi_callable import UnaryUnary, UnaryStream, StreamUnary, StreamStream

__all__ = ["async_testing_channel"]


class AsyncChannel(six.with_metaclass(abc.ABCMeta, grpc.aio.Channel)):
    """A grpc.aio.Channel double with which to test a system that invokes RPCs."""

    @abc.abstractmethod
    def take_unary_unary(self, method_descriptor):
        """Draws an RPC currently being made by the system under test.

        If the given descriptor does not identify any RPC currently being made
        by the system under test, this method blocks until the system under
        test invokes such an RPC.

        Args:
          method_descriptor: A descriptor.MethodDescriptor describing a
            unary-unary RPC method.

        Returns:
          A (invocation_metadata, request, unary_unary_channel_rpc) tuple of
            the RPC's invocation metadata, its request, and a
            UnaryUnaryChannelRpc with which to "play server" for the RPC.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def take_unary_stream(self, method_descriptor):
        """Draws an RPC currently being made by the system under test.

        If the given descriptor does not identify any RPC currently being made
        by the system under test, this method blocks until the system under
        test invokes such an RPC.

        Args:
          method_descriptor: A descriptor.MethodDescriptor describing a
            unary-stream RPC method.

        Returns:
          A (invocation_metadata, request, unary_stream_channel_rpc) tuple of
            the RPC's invocation metadata, its request, and a
            UnaryStreamChannelRpc with which to "play server" for the RPC.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def take_stream_unary(self, method_descriptor):
        """Draws an RPC currently being made by the system under test.

        If the given descriptor does not identify any RPC currently being made
        by the system under test, this method blocks until the system under
        test invokes such an RPC.

        Args:
          method_descriptor: A descriptor.MethodDescriptor describing a
            stream-unary RPC method.

        Returns:
          A (invocation_metadata, stream_unary_channel_rpc) tuple of the RPC's
            invocation metadata and a StreamUnaryChannelRpc with which to "play
            server" for the RPC.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def take_stream_stream(self, method_descriptor):
        """Draws an RPC currently being made by the system under test.

        If the given descriptor does not identify any RPC currently being made
        by the system under test, this method blocks until the system under
        test invokes such an RPC.

        Args:
          method_descriptor: A descriptor.MethodDescriptor describing a
            stream-stream RPC method.

        Returns:
          A (invocation_metadata, stream_stream_channel_rpc) tuple of the RPC's
            invocation metadata and a StreamStreamChannelRpc with which to
            "play server" for the RPC.
        """
        raise NotImplementedError()


class TestingAsyncChannel(AsyncChannel):
    def __init__(self, time, state: State):
        self._time = time
        self._state = state

    def subscribe(self, callback, try_to_connect=False):
        raise NotImplementedError()

    def unsubscribe(self, callback):
        raise NotImplementedError()

    def unary_unary(self,
                    method,
                    request_serializer=None,
                    response_deserializer=None):
        return UnaryUnary(method, self._state)

    def unary_stream(self,
                     method,
                     request_serializer=None,
                     response_deserializer=None):
        return UnaryStream(method, self._state)

    def stream_unary(self,
                     method,
                     request_serializer=None,
                     response_deserializer=None):
        return StreamUnary(method, self._state)

    def stream_stream(self,
                      method,
                      request_serializer=None,
                      response_deserializer=None):
        return StreamStream(method, self._state)

    def _close(self):
        # TODO(https://github.com/grpc/grpc/issues/12531): Decide what
        # action to take here, if any?
        pass

    async def close(self, grace=None):
        self._close()

    def take_unary_unary(self, method_descriptor):
        return _channel_rpc.unary_unary(self._state, method_descriptor)

    def take_unary_stream(self, method_descriptor):
        return _channel_rpc.unary_stream(self._state, method_descriptor)

    def take_stream_unary(self, method_descriptor):
        return _channel_rpc.stream_unary(self._state, method_descriptor)

    def take_stream_stream(self, method_descriptor):
        return _channel_rpc.stream_stream(self._state, method_descriptor)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._close()

    async def channel_ready(self) -> None:
        return

    def get_state(self,
                  try_to_connect: bool = False) -> grpc.ChannelConnectivity:
        return grpc.ChannelConnectivity.READY

    async def wait_for_state_change(
        self,
        last_observed_state: grpc.ChannelConnectivity,
    ) -> None:
        await asyncio.sleep(0)


def async_testing_channel(descriptors, time):
    return TestingAsyncChannel(time, _channel_state.State())
