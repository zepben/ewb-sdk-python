#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Callable, Optional, Iterator, Tuple
from datetime import datetime

from zepben.protobuf.ns.network_state_pb2_grpc import QueryNetworkStateServiceServicer
from zepben.protobuf.ns.network_state_requests_pb2 import GetCurrentStatesRequest
from zepben.protobuf.ns.network_state_responses_pb2 import GetCurrentStatesResponse
from zepben.evolve.streaming.data.current_state_event import CurrentStateEvent

GetCurrentStates = Callable[[Optional[datetime], Optional[datetime]], Iterator[Tuple[CurrentStateEvent, ...]]]

class QueryNetworkStateService(QueryNetworkStateServiceServicer):
    def __init__(self, on_get_current_states: GetCurrentStates):
        self.on_get_current_states = on_get_current_states

    def getCurrentStates(self, request: GetCurrentStatesRequest, context) -> Iterator[GetCurrentStatesResponse]:
        for events in self.on_get_current_states(request.fromTimestamp.ToDatetime(), request.toTimestamp.ToDatetime()):
            yield GetCurrentStatesResponse(messageId=request.messageId, event=[event.to_pb() for event in events])