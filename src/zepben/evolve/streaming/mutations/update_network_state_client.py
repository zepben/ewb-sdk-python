#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["UpdateNetworkStateClient"]

from dataclasses import dataclass
from typing import List, Callable, AsyncGenerator, Iterable

from zepben.protobuf.ns.network_state_pb2_grpc import UpdateNetworkStateServiceStub
from zepben.protobuf.ns.network_state_requests_pb2 import SetCurrentStatesRequest as PBSetCurrentStatesRequest

from zepben.evolve.streaming.data.current_state_event import CurrentStateEvent
from zepben.evolve.streaming.data.set_current_states_status import SetCurrentStatesStatus
from zepben.evolve.streaming.grpc.grpc import GrpcClient


class UpdateNetworkStateClient(GrpcClient):
    """
    A client class that provides functionality to interact with the gRPC service for updating network states.
    A gRPC channel or stub must be provided.
    """

    _stub: UpdateNetworkStateServiceStub = None

    def __init__(self, channel=None, stub: UpdateNetworkStateServiceStub = None, error_handlers: List[Callable[[Exception], bool]] = None, timeout: int = 60):
        super().__init__(error_handlers=error_handlers, timeout=timeout)
        if channel is None and stub is None:
            raise ValueError("Must provide either a channel or a stub")
        if stub is not None:
            self._stub = stub
        else:
            self._stub = UpdateNetworkStateServiceStub(channel)

    async def set_current_states(self, batch_id: int, batch: Iterable[CurrentStateEvent]) -> SetCurrentStatesStatus:
        """
        Sends a single batch of current state events to the gRPC service for processing.

        This method allows for sending a single batch of current state events to the gRPC service using the gRPC stub provided in the constructor.

        Args:
            batch_id: A unique identifier for the batch of events being processed.
            batch: A collection of CurrentStateEvent objects representing a single batch of events
                                             to be processed by the gRPC service.

        Returns:
            A SetCurrentStatesResponse object representing the status of the batch after being processed by the service.
        """

        async def request_generator() -> AsyncGenerator['UpdateNetworkStateClient.SetCurrentStatesRequest', None]:
            yield UpdateNetworkStateClient.SetCurrentStatesRequest(batch_id, batch)

        responses = [response async for response in self.set_current_states_in_batches(request_generator())]
        if len(responses) == 0:
            raise RuntimeError(f"There are no response for this batch {batch_id}")

        return responses[0]

    async def set_current_states_in_batches(self, batches: AsyncGenerator['UpdateNetworkStateClient.SetCurrentStatesRequest', None]) -> AsyncGenerator[
        SetCurrentStatesStatus, None]:
        """
        Sends a stream of current state events to the gRPC service for processing.

        This method is responsible for streaming a batch of current state events to the gRPC service using the gRPC stub provided in the constructor.

        Args:
            batches: A stream of SetCurrentStatesRequest objects, where each request contains a
                     collection of CurrentStateEvent objects to be processed by the gRPC service.

        Returns:
            A stream of SetCurrentStatesResponse objects representing the status of each batch after being processed by the gRPC service.
        """

        async def request_generator():
            async for batch in batches:
                yield PBSetCurrentStatesRequest(messageId=batch.batch_id, event=[event.to_pb() for event in batch.events])

        async for response in self._stub.setCurrentStates(request_generator()):
            yield SetCurrentStatesStatus.from_pb(response)

    @dataclass
    class SetCurrentStatesRequest:
        """
        A request object for submitting a batch of current state events for processing.

        Attributes:
            batch_id: A unique identifier for the batch of events being processed. This allows tracking or grouping multiple events under a single batch.
            events: A list of CurrentStateEvent objects representing the state changes or events that are being submitted in the current batch.
        """

        batch_id: int
        events: Iterable[CurrentStateEvent]
