#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["QueryNetworkStateService"]

from datetime import datetime
from typing import Callable, AsyncGenerator, Iterable

from zepben.protobuf.ns.network_state_pb2_grpc import QueryNetworkStateServiceServicer
from zepben.protobuf.ns.network_state_requests_pb2 import GetCurrentStatesRequest
from zepben.protobuf.ns.network_state_responses_pb2 import GetCurrentStatesResponse

from zepben.evolve.streaming.data.current_state_event import CurrentStateEvent


class QueryNetworkStateService(QueryNetworkStateServiceServicer):
    """
    A service class that provides a simplified interface for retrieving current state events
    via gRPC without exposing the underlying complexity of gRPC mechanisms.

    This class serves as a wrapper around the gRPC-generated service implementation,
    allowing users to interact with it using a more convenient function type.

    Attributes:
        on_get_current_states: An function that retrieves CurrentStateEvent objects within the specified time range.
    """

    def __init__(self, on_get_current_states: Callable[[datetime, datetime], AsyncGenerator[Iterable[CurrentStateEvent], None]]):
        self.on_get_current_states = on_get_current_states

    async def getCurrentStates(self, request: GetCurrentStatesRequest, context) -> AsyncGenerator[GetCurrentStatesResponse, None]:
        """
        Handles the incoming request for retrieving current state events.

        This method processes the provided GetCurrentStatesRequest, retrieves the
        corresponding current state events using the callback function passed in
        the constructor, and asynchronously returns a GetCurrentStatesResponse.
        It acts as a bridge between the gRPC request and the business logic that fetches the current state events.

        Args:
            request: The request object containing parameters for fetching current state events,
            including the time range for the query.
            context: The gRPC context.

        Returns:
           A stream of gRPC response message
        """
        async for events in self.on_get_current_states(request.fromTimestamp.ToDatetime(), request.toTimestamp.ToDatetime()):
            yield GetCurrentStatesResponse(messageId=request.messageId, event=[event.to_pb() for event in events])
