#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Tuple, Callable, AsyncGenerator

from zepben.protobuf.ns.network_state_pb2_grpc import UpdateNetworkStateServiceServicer

from zepben.evolve.streaming.data.current_state_event import CurrentStateEvent
from zepben.evolve.streaming.data.set_current_states_status import BatchSuccessful, ProcessingPaused, BatchFailure, SetCurrentStatesStatus
from zepben.protobuf.ns.network_state_requests_pb2 import SetCurrentStatesRequest as PBSetCurrentStatesRequest
from zepben.protobuf.ns.network_state_responses_pb2 import SetCurrentStatesResponse as PBSetCurrentStatesResponse


class UpdateNetworkStateService(UpdateNetworkStateServiceServicer):

    def __init__(self, on_set_current_states: Callable[
        [AsyncGenerator[Tuple[int, Tuple[CurrentStateEvent, ...]], None]], AsyncGenerator[SetCurrentStatesStatus, None]]):
        self.on_set_current_states = on_set_current_states

    async def setCurrentStates(self, request_iterator: AsyncGenerator[PBSetCurrentStatesRequest, None], context) -> AsyncGenerator[
        PBSetCurrentStatesResponse, None]:
        async def request_generator() -> AsyncGenerator[Tuple[int, Tuple[CurrentStateEvent, ...]], None]:
            async for request in request_iterator:
                yield request.messageId, tuple([CurrentStateEvent.from_pb(event) for event in request.event])

        async for status in self.on_set_current_states(request_generator()):
            match status:
                case BatchSuccessful() as status:
                    yield PBSetCurrentStatesResponse(messageId=1, success=status.to_pb())  # TODO: Update SetCurrentStatesStatus to have the batch id
                case ProcessingPaused() as status:
                    yield PBSetCurrentStatesResponse(messageId=1, paused=status.to_pb())
                case BatchFailure() as status:
                    yield PBSetCurrentStatesResponse(messageId=1, failure=status.to_pb())
