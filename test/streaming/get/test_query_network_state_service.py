#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from collections.abc import AsyncGenerator
from typing import Tuple

import grpc
import pytest
from datetime import datetime, timedelta

from zepben.protobuf.ns.network_state_requests_pb2 import GetCurrentStatesRequest

from util import grpc_aio_server
from zepben.evolve import datetime_to_timestamp
from zepben.evolve.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.protobuf.ns.network_state_pb2_grpc import QueryNetworkStateServiceStub, add_QueryNetworkStateServiceServicer_to_server
from zepben.evolve.streaming.data.current_state_event import SwitchStateEvent, SwitchAction, CurrentStateEvent
from zepben.evolve.streaming.get.query_network_state_service import QueryNetworkStateService

class TestQueryNetworkStateService:

    from_datetime = datetime.now()
    to_datetime = datetime.now() + timedelta(days=1)
    current_state_events = (
        (SwitchStateEvent("event1", datetime.now(), "mrid1", SwitchAction.OPEN, PhaseCode.ABC),),
        (SwitchStateEvent("event2", datetime.now(), "mrid1", SwitchAction.CLOSE, PhaseCode.ABN),),
        (SwitchStateEvent("event3", datetime.now(), "mrid2", SwitchAction.CLOSE, PhaseCode.A),)
    )

    @pytest.fixture
    async def grpc_stub(self):
        async def on_get_current_states(from_datetime: datetime, to_datetime: datetime) -> AsyncGenerator[Tuple[CurrentStateEvent, ...], None]:
            assert from_datetime == self.from_datetime
            assert to_datetime == self.to_datetime
            for event in self.current_state_events:
                yield event

        server, host = grpc_aio_server()
        add_QueryNetworkStateServiceServicer_to_server(QueryNetworkStateService(on_get_current_states), server)

        await server.start()
        async with grpc.aio.insecure_channel(host) as channel:
            yield QueryNetworkStateServiceStub(channel)

        await server.stop(None)

    @pytest.mark.asyncio
    async def test_get_current_states(self, grpc_stub):
        request = GetCurrentStatesRequest(messageId=1, fromTimestamp=datetime_to_timestamp(self.from_datetime),
                                          toTimestamp=datetime_to_timestamp(self.to_datetime))
        responses = [response async for response in grpc_stub.getCurrentStates(request)]

        expected_result = [event for batch in self.current_state_events for event in batch]
        actual_result = [event for response in responses for event in response.event]

        assert [a.messageId for a in responses] == [1, 1, 1]
        assert [a.eventId for a in actual_result] == [e.event_id for e in expected_result]
        assert [a.timestamp for a in actual_result] == [datetime_to_timestamp(e.timestamp) for e in expected_result]
        assert [a.switch.mRID for a in actual_result] == [e.mRID for e in expected_result]
        assert [a.switch.action for a in actual_result] == [e.action.value for e in expected_result]
        assert [a.switch.phases for a in actual_result] == [e.phases.value[0] for e in expected_result]
