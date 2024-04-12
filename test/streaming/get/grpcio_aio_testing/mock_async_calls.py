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
from abc import ABC
from typing import TypeVar, Union, AsyncIterable, Optional

import grpc
from grpc.aio import UnaryUnaryCall, StreamUnaryCall, UnaryStreamCall, StreamStreamCall, Metadata

__all__ = ["UnaryResponse", "ResponseIteratorCall"]

from grpc.aio._typing import RequestType, DoneCallbackType

from grpc_testing._channel._invocation import _RpcErrorCall, _initial_metadata, _trailing_metadata, _code, _details, _add_callback, _time_remaining, \
    _is_active, _cancel

ResponseType = TypeVar("ResponseType")
EOFType = TypeVar("EOFType")


class UnaryResponse(UnaryUnaryCall, StreamUnaryCall, ABC):
    async def write(self, request: RequestType) -> None:
        pass

    async def done_writing(self) -> None:
        pass

    async def initial_metadata(self) -> Metadata:
        return _initial_metadata(self._handler)

    async def trailing_metadata(self) -> Metadata:
        return _trailing_metadata(self._handler)

    async def code(self) -> grpc.StatusCode:
        return _code(self._handler)

    async def details(self) -> str:
        return _details(self._handler)

    async def wait_for_connection(self) -> None:
        pass

    def cancelled(self) -> bool:
        return False

    def done(self) -> bool:
        return True

    def time_remaining(self) -> Optional[float]:
        return _time_remaining(self._handler)

    def cancel(self) -> bool:
        return _cancel(self._handler)

    def add_done_callback(self, callback: DoneCallbackType) -> None:
        return _add_callback(self._handler, callback)

    def __init__(self, rpc_handler):
        self._handler = rpc_handler

    def __await__(self):
        return self._response().__await__()

    async def _response(self):
        read = self._handler.take_response()
        if read.code is None:
            unused_trailing_metadata, code, unused_details = self._handler.termination()
            if code is grpc.StatusCode.OK:
                return read.response
            else:
                raise _RpcErrorCall(self._handler)
        else:
            raise _RpcErrorCall(self._handler)


class ResponseIteratorCall(UnaryStreamCall, StreamStreamCall, ABC):
    def __init__(self, rpc_handler):
        self._handler = rpc_handler

    def __aiter__(self) -> AsyncIterable[ResponseType]:
        return self

    async def __anext__(self) -> ResponseType:
        read = self._handler.take_response()
        if read.code is None:
            return read.response
        elif read.code is grpc.StatusCode.OK:
            raise StopAsyncIteration
        else:
            raise _RpcErrorCall(self._handler)

    def cancel(self):
        _cancel(self._handler)

    def is_active(self):
        return _is_active(self._handler)

    def time_remaining(self):
        return _time_remaining(self._handler)

    def add_callback(self, callback):
        return _add_callback(self._handler, callback)

    def initial_metadata(self):
        return _initial_metadata(self._handler)

    def trailing_metadata(self):
        return _trailing_metadata(self._handler)

    def code(self):
        return _code(self._handler)

    def details(self):
        return _details(self._handler)

    async def wait_for_connection(self) -> None:
        pass

    def cancelled(self) -> bool:
        return False

    def done(self) -> bool:
        return True

    def add_done_callback(self, callback: DoneCallbackType) -> None:
        pass

    async def read(self) -> Union[EOFType, ResponseType]:
        read = self._handler.take_response()
        if read.code is None:
            return read.response
        elif read.code is grpc.StatusCode.OK:
            return grpc.aio.EOF
        else:
            raise _RpcErrorCall(self._handler)

    async def write(self, request: RequestType) -> None:
        pass

    async def done_writing(self) -> None:
        pass
