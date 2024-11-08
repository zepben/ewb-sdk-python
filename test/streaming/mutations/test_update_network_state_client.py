#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import datetime
from typing import AsyncGenerator

import grpc
import pytest
from zepben.protobuf.ns.data.change_status_pb2 import BatchSuccessful as PBBatchSuccessful, ProcessingPaused as PBProcessingPaused, \
    BatchFailure as PBBatchFailure
from zepben.protobuf.ns.network_state_pb2_grpc import UpdateNetworkStateServiceServicer, add_UpdateNetworkStateServiceServicer_to_server
from zepben.protobuf.ns.network_state_requests_pb2 import SetCurrentStatesRequest as PBSetCurrentStatesRequest
from zepben.protobuf.ns.network_state_responses_pb2 import SetCurrentStatesResponse as PBSetCurrentStatesResponse

from util import grpc_aio_server
from zepben.evolve import PhaseCode
from zepben.evolve.streaming.data.current_state_event import SwitchStateEvent, SwitchAction, CurrentStateEvent
from zepben.evolve.streaming.data.set_current_states_status import BatchSuccessful, ProcessingPaused, BatchFailure
from zepben.evolve.streaming.mutations.update_network_state_client import UpdateNetworkStateClient


class MockUpdateNetworkStateService(UpdateNetworkStateServiceServicer):
    responses = {
        1: PBSetCurrentStatesResponse(messageId=1, success=PBBatchSuccessful()),
        2: PBSetCurrentStatesResponse(messageId=2, paused=PBProcessingPaused()),
        3: PBSetCurrentStatesResponse(messageId=3, failure=PBBatchFailure())
    }

    def __init__(self):
        self.requests = []

    async def setCurrentStates(self, request_iterator: AsyncGenerator[PBSetCurrentStatesRequest, None], context):
        async for request in request_iterator:
            self.requests.append(request)
            yield self.responses[request.messageId]


class TestUpdateNetworkStateClient:
    current_state_events = (
        SwitchStateEvent("event1", datetime.now(), "mrid1", SwitchAction.OPEN, PhaseCode.ABC),
        SwitchStateEvent("event2", datetime.now(), "mrid1", SwitchAction.CLOSE, PhaseCode.ABN),
        SwitchStateEvent("event3", datetime.now(), "mrid2", SwitchAction.CLOSE, PhaseCode.A)
    )

    @pytest.fixture
    async def grpc_service_client_pair(self):
        server, host = grpc_aio_server()
        service = MockUpdateNetworkStateService()
        add_UpdateNetworkStateServiceServicer_to_server(service, server)
        await server.start()
        async with grpc.aio.insecure_channel(host) as channel:
            yield service, UpdateNetworkStateClient(channel)

        await server.stop(None)

    @pytest.mark.asyncio
    async def test_set_current_state(self, grpc_service_client_pair):
        service, client = grpc_service_client_pair
        result = await client.set_current_states(1, self.current_state_events)

        request = service.requests[0]
        assert request.messageId == 1
        assert tuple([CurrentStateEvent.from_pb(event) for event in request.event]) == self.current_state_events

        assert result.batch_id == 1
        assert isinstance(result, BatchSuccessful)

    @pytest.mark.asyncio
    async def test_set_current_states_in_batches(self, grpc_service_client_pair):
        service, client = grpc_service_client_pair

        async def generate_requests() -> AsyncGenerator[PBSetCurrentStatesRequest, None]:
            for i in range(3):
                yield UpdateNetworkStateClient.SetCurrentStatesRequest(batch_id=i + 1, events=self.current_state_events)

        result = [response async for response in client.set_current_states_in_batches(generate_requests())]

        assert [request.messageId for request in service.requests] == [1, 2, 3]
        for request in service.requests:
            assert tuple([CurrentStateEvent.from_pb(event) for event in request.event]) == self.current_state_events

        assert [r.batch_id for r in result] == [1, 2, 3]
        assert isinstance(result[0], BatchSuccessful)
        assert isinstance(result[1], ProcessingPaused)
        assert isinstance(result[2], BatchFailure)
