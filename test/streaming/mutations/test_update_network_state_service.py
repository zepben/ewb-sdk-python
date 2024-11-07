#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import datetime
from typing import AsyncGenerator, Tuple

import grpc
import pytest
from zepben.protobuf.ns.network_state_pb2_grpc import add_UpdateNetworkStateServiceServicer_to_server, UpdateNetworkStateServiceStub

from util import grpc_aio_server
from zepben.evolve import PhaseCode
from zepben.evolve.streaming.data.current_state_event import SwitchStateEvent, SwitchAction, CurrentStateEvent
from zepben.evolve.streaming.data.set_current_states_status import SetCurrentStatesStatus, BatchSuccessful, ProcessingPaused, BatchFailure
from zepben.evolve.streaming.mutations.update_network_state_service import UpdateNetworkStateService
from zepben.protobuf.ns.network_state_requests_pb2 import SetCurrentStatesRequest as PBSetCurrentStatesRequest


class TestUpdateNetworkStateService:

    current_state_events = (
        (SwitchStateEvent("event1", datetime.now(), "mrid1", SwitchAction.OPEN, PhaseCode.ABC),),
        (SwitchStateEvent("event2", datetime.now(), "mrid1", SwitchAction.CLOSE, PhaseCode.ABN),),
        (SwitchStateEvent("event3", datetime.now(), "mrid2", SwitchAction.CLOSE, PhaseCode.A),)
    )

    expected_results = {
        1: BatchSuccessful(batch_id=1),
        2: ProcessingPaused(batch_id=2, since=datetime.now()),
        3: BatchFailure(batch_id=3, partial_failure=False, failures=())
    }

    @pytest.fixture
    async def grpc_stub(self):
        async def on_set_current_states(batches: AsyncGenerator[Tuple[int, Tuple[CurrentStateEvent, ...]], None]) -> AsyncGenerator[
            SetCurrentStatesStatus, None]:
            async for batch_id, events in batches:
                assert events == self.current_state_events[batch_id - 1]
                yield self.expected_results[batch_id]

        server, host = grpc_aio_server()
        add_UpdateNetworkStateServiceServicer_to_server(UpdateNetworkStateService(on_set_current_states), server)

        await server.start()
        async with grpc.aio.insecure_channel(host) as channel:
            yield UpdateNetworkStateServiceStub(channel)

        await server.stop(None)

    @pytest.mark.asyncio
    async def test_set_current_states(self, grpc_stub):
        async def request_generator():
            for batch_id in range(3):
                yield PBSetCurrentStatesRequest(messageId=batch_id + 1, event=[event.to_pb() for event in self.current_state_events[batch_id]])

        expected_results = [status for status in self.expected_results.values()]
        actual_result = [result async for result in grpc_stub.setCurrentStates(request_generator())]

        assert [result.messageId for result in actual_result] == [1, 2, 3]
        for actual, expected in zip(actual_result, expected_results):
            assert SetCurrentStatesStatus.from_pb(actual) == expected
