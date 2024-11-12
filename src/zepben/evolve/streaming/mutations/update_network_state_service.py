#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["UpdateNetworkStateService"]

from typing import Tuple, Callable, AsyncGenerator

from zepben.protobuf.ns.network_state_pb2_grpc import UpdateNetworkStateServiceServicer
from zepben.protobuf.ns.network_state_requests_pb2 import SetCurrentStatesRequest as PBSetCurrentStatesRequest
from zepben.protobuf.ns.network_state_responses_pb2 import SetCurrentStatesResponse as PBSetCurrentStatesResponse

from zepben.evolve.streaming.data.current_state_event import CurrentStateEvent
from zepben.evolve.streaming.data.set_current_states_status import SetCurrentStatesStatus


class UpdateNetworkStateService(UpdateNetworkStateServiceServicer):
    """
    A service class that provides a simplified interface for updating network state events
    via gRPC without exposing the underlying complexity of gRPC mechanisms.

    This class serves as a wrapper around the gRPC-generated service implementation,
    allowing users to update the network state using a more convenient function type.

    Attributes:
        on_set_current_states: A function that takes CurrentStateEvent objects asynchronously and returns a
                               SetCurrentStatesStatus asynchronously that reflects the success or failure of the batch
                               update process.
    """

    def __init__(self, on_set_current_states: Callable[
        [AsyncGenerator[Tuple[int, Tuple[CurrentStateEvent, ...]], None]], AsyncGenerator[SetCurrentStatesStatus, None]]):
        self.on_set_current_states = on_set_current_states

    async def setCurrentStates(self, request_iterator: AsyncGenerator[PBSetCurrentStatesRequest, None], context) -> AsyncGenerator[
        PBSetCurrentStatesResponse, None]:
        """
        Handles streaming requests for setting current state events and responds with the result of the operation.

        This method is a bidirectional streaming gRPC implementation that processes incoming
        SetCurrentStatesRequest objects from the client, applies the provided state events using the callback function
        passed in the constructor, and sends back a SetCurrentStatesResponse indicating the outcome of the update operation.

        It allows clients to stream multiple state events for asynchronous processing. As each event is processed,
        the service responds with the status of the operation in real-time, without waiting for all events to be received.

        Args:
            request_iterator: The stream of protobuf requests to process.
            context: The gRPC context.

        Returns:
            A stream of protobuf SetCurrentStatesResponse sent back.
        """

        async def request_generator() -> AsyncGenerator[Tuple[int, Tuple[CurrentStateEvent, ...]], None]:
            async for request in request_iterator:
                yield request.messageId, tuple([CurrentStateEvent.from_pb(event) for event in request.event])

        async for status in self.on_set_current_states(request_generator()):
            yield status.to_pb()
