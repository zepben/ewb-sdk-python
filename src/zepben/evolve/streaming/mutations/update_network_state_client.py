#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import asyncio
from typing import List, Callable, AsyncGenerator, Tuple, overload

from attr import dataclass
from zepben.protobuf.ns.network_state_pb2_grpc import UpdateNetworkStateServiceStub
from zepben.protobuf.ns.network_state_requests_pb2 import SetCurrentStatesRequest as PBSetCurrentStatesRequest

from zepben.evolve.streaming.data.current_state_event import CurrentStateEvent
from zepben.evolve.streaming.data.set_current_states_status import SetCurrentStatesStatus, BatchSuccessful, ProcessingPaused, BatchFailure
from zepben.evolve.streaming.grpc.grpc import GrpcClient


class UpdateNetworkStateClient(GrpcClient):
    _stub: UpdateNetworkStateServiceStub = None

    def __init__(self, channel=None, stub: UpdateNetworkStateServiceStub = None, error_handlers: List[Callable[[Exception], bool]] = None, timeout: int = 60):
        super().__init__(error_handlers=error_handlers, timeout=timeout)
        if channel is None and stub is None:
            raise ValueError("Must provide either a channel or a stub")
        if stub is not None:
            self._stub = stub
        else:
            self._stub = UpdateNetworkStateServiceStub(channel)

    async def set_current_states(self, batch_id: int, batch: Tuple[CurrentStateEvent, ...]) -> 'UpdateNetworkStateClient.SetCurrentStatesResponse':
        async def request_generator() -> AsyncGenerator['UpdateNetworkStateClient.SetCurrentStatesRequest', None]:
            yield UpdateNetworkStateClient.SetCurrentStatesRequest(batch_id, batch)

        responses = [response async for response in self.set_current_states_in_batches(request_generator())]
        if len(responses) == 0:
            raise RuntimeError(f"There are no response for this batch {batch_id}")

        return responses[0]

    async def set_current_states_in_batches(self, batches: AsyncGenerator['UpdateNetworkStateClient.SetCurrentStatesRequest', None]) -> AsyncGenerator[
        'UpdateNetworkStateClient.SetCurrentStatesResponse', None]:
        async def request_generator():
            async for batch in batches:
                yield PBSetCurrentStatesRequest(messageId=batch.batch_id, event=[event.to_pb() for event in batch.events])

        async for response in self._stub.setCurrentStates(request_generator()):
            match response.WhichOneof("status"):
                case "success":
                    status = BatchSuccessful.from_pb(response.success)
                case "paused":
                    status = ProcessingPaused.from_pb(response.paused)
                case "failure":
                    status = BatchFailure.from_pb(response.failure)
                case _:
                    status = None

            yield UpdateNetworkStateClient.SetCurrentStatesResponse(batch_id=response.messageId, status=status)

    @dataclass
    class SetCurrentStatesRequest:
        batch_id: int
        events: Tuple[CurrentStateEvent, ...]

    @dataclass
    class SetCurrentStatesResponse:
        batch_id: int
        status: SetCurrentStatesStatus
