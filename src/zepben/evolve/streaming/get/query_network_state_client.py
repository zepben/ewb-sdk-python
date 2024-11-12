#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["QueryNetworkStateClient"]

from datetime import datetime
from typing import List, Callable, AsyncGenerator, Tuple

from zepben.protobuf.ns.network_state_pb2_grpc import QueryNetworkStateServiceStub
from zepben.protobuf.ns.network_state_requests_pb2 import GetCurrentStatesRequest

from zepben.evolve.util import datetime_to_timestamp
from zepben.evolve.streaming.data.current_state_event import CurrentStateEvent
from zepben.evolve.streaming.grpc.grpc import GrpcClient


class QueryNetworkStateClient(GrpcClient):
    """
    A client class that provides functionality to interact with the gRPC service for querying network states.
    A gRPC channel or stub must be provided.
    """

    _stub: QueryNetworkStateServiceStub = None

    def __init__(self, channel=None, stub: QueryNetworkStateServiceStub = None, error_handlers: List[Callable[[Exception], bool]] = None, timeout: int = 60):
        super().__init__(error_handlers=error_handlers, timeout=timeout)
        if channel is None and stub is None:
            raise ValueError("Must provide either a channel or a stub")
        if stub is not None:
            self._stub = stub
        else:
            self._stub = QueryNetworkStateServiceStub(channel)

    async def get_current_states(self, query_id: int, from_datetime: datetime, to_datetime: datetime) -> AsyncGenerator[Tuple[CurrentStateEvent, ...], None]:
        """
        Asynchronously retrieves a collection containing CurrentStateEvent objects, representing the network states
        within a specified time range.

        Args:
            query_id: A unique identifier for the query being processed.
            from_datetime: The start time, as a datetime, for the query range.
            to_datetime: The end time, as a datetime, for the query range.

        Returns:
            A stream of batched network state events in the specified time range.
        """
        async for response in self._stub.getCurrentStates(
            GetCurrentStatesRequest(messageId=query_id, fromTimestamp=datetime_to_timestamp(from_datetime), toTimestamp=datetime_to_timestamp(to_datetime))):
            yield [CurrentStateEvent.from_pb(event) for event in response.event]
