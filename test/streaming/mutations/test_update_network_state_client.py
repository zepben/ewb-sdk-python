#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import datetime
from typing import AsyncGenerator

import grpc
import pytest
from zepben.protobuf.ns.network_state_pb2_grpc import UpdateNetworkStateServiceServicer, add_UpdateNetworkStateServiceServicer_to_server

from util import grpc_server
from zepben.evolve import PhaseCode
from zepben.evolve.streaming.data.current_state_event import SwitchStateEvent, SwitchAction
from zepben.evolve.streaming.mutations.update_network_state_client import UpdateNetworkStateClient
from zepben.protobuf.ns.network_state_responses_pb2 import SetCurrentStatesResponse as PBSetCurrentStatesResponse
from zepben.protobuf.ns.data.change_status_pb2 import BatchSuccessful as PBBatchSuccessful, BatchSuccessful
from zepben.protobuf.ns.network_state_requests_pb2 import SetCurrentStatesRequest as PBSetCurrentStatesRequest

class MockUpdateNetworkStateService(UpdateNetworkStateServiceServicer):
    async def setCurrentStates(self, request_iterator: AsyncGenerator[PBSetCurrentStatesRequest, None], context):
        async for request in request_iterator:
            yield PBSetCurrentStatesResponse(messageId=request.messageId, success=PBBatchSuccessful())


class TestUpdateNetworkStateClient:

    current_state_events = (
        SwitchStateEvent("event1", datetime.now(), "mrid1", SwitchAction.OPEN, PhaseCode.ABC),
        SwitchStateEvent("event2", datetime.now(), "mrid1", SwitchAction.CLOSE, PhaseCode.ABN),
        SwitchStateEvent("event3", datetime.now(), "mrid2", SwitchAction.CLOSE, PhaseCode.A)
    )

    @pytest.fixture
    async def client(self):
        server, host = grpc_server()
        add_UpdateNetworkStateServiceServicer_to_server(MockUpdateNetworkStateService(), server)
        await server.start()
        async with grpc.aio.insecure_channel(host) as channel:
            client = UpdateNetworkStateClient(channel)
            yield client

        await server.stop(None)

    @pytest.mark.asyncio
    async def test_set_current_state(self, client):
        result = await client.set_current_states(1, self.current_state_events)

        assert result.batch_id == 1
        assert isinstance(result.status, BatchSuccessful)

    @pytest.mark.asyncio
    async def test_set_current_state(self, client):
        async def generate_requests() -> AsyncGenerator[PBSetCurrentStatesRequest, None]:
            for i in range(3):
                yield UpdateNetworkStateClient.SetCurrentStatesRequest(batch_id=i, events=self.current_state_events)

        result = [response async for response in client.set_current_states_in_batches(generate_requests())]
        assert len(result) == 3