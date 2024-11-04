#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from datetime import datetime

from google.protobuf.timestamp_pb2 import Timestamp
from zepben.protobuf.ns.network_state_pb2_grpc import QueryNetworkStateServiceStub
from typing import List, Callable, AsyncGenerator, Tuple

from zepben.protobuf.ns.network_state_requests_pb2 import GetCurrentStatesRequest
from zepben.evolve.streaming.data.current_state_event import CurrentStateEvent
from zepben.evolve.streaming.grpc.grpc import GrpcClient

class QueryNetworkStateClient(GrpcClient):

    _stub: QueryNetworkStateServiceStub = None

    def __init__(self, channel = None, stub: QueryNetworkStateServiceStub = None, error_handlers: List[Callable[[Exception], bool]] = None, timeout: int = 60):
        super().__init__(error_handlers=error_handlers, timeout=timeout)
        if channel is None and stub is None:
            raise ValueError("Must provide either a channel or a stub")
        if stub is not None:
            self._stub = stub
        else:
            self._stub = QueryNetworkStateServiceStub(channel)

    async def get_current_states(self, queryId: int, fromDatetime: datetime, toDatetime: datetime) -> AsyncGenerator[Tuple[CurrentStateEvent, ...], None]:
        fromTimestamp = Timestamp()
        fromTimestamp.FromDatetime(fromDatetime)
        toTimestamp = Timestamp()
        toTimestamp.FromDatetime(toDatetime)
        async for response in self._stub.getCurrentStates(GetCurrentStatesRequest(messageId=queryId, fromTimestamp=fromTimestamp, toTimestamp=toTimestamp)):
            yield [CurrentStateEvent._from_pb(event) for event in response.event]

