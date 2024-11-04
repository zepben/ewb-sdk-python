#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List, Iterable, Callable, Generator

import grpc_testing
import pytest
from datetime import datetime, timezone

from google.protobuf.timestamp_pb2 import Timestamp
from zepben.protobuf.ns.network_state_requests_pb2 import GetCurrentStatesRequest

from zepben.evolve.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.protobuf.ns.network_state_pb2_grpc import QueryNetworkStateServiceStub
from zepben.protobuf.ns import network_state_pb2

from streaming.get.grpcio_aio_testing.mock_async_channel import async_testing_channel
from streaming.get.mock_server import MockServer, StreamGrpc, GrpcResponse, GrpcRequest
from zepben.evolve.streaming.data.current_state_event import SwitchStateEvent, SwitchAction
from zepben.evolve.streaming.get.query_network_state_service import QueryNetworkStateService, GetCurrentStates
from unittest.mock import Mock


class TestQueryNetworkStateService:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.channel = async_testing_channel(network_state_pb2.DESCRIPTOR.services_by_name.values(), grpc_testing.strict_real_time())
        self.mock_server = MockServer(self.channel, network_state_pb2.DESCRIPTOR.services_by_name['QueryNetworkStateService'])
        self.stub = QueryNetworkStateServiceStub(self.channel)
        self.on_get_current_states = Mock()
        self.current_state_events = (
            (SwitchStateEvent("event1", datetime.now(), "mrid1", SwitchAction.OPEN, PhaseCode.ABC),),
            (SwitchStateEvent("event2", datetime.now(), "mrid1", SwitchAction.CLOSE, PhaseCode.ABN),),
            (SwitchStateEvent("event3", datetime.now(), "mrid2", SwitchAction.CLOSE, PhaseCode.A),)
        )
        self.on_get_current_states.return_value = iter(self.current_state_events)
        self.service = QueryNetworkStateService(self.on_get_current_states)

    @pytest.mark.asyncio
    async def test_get_current_states(self):
        def call_service() -> List[Callable[[GrpcRequest], Generator[GrpcResponse, None, None]]]:
            def process(request: GrpcRequest) -> Generator[GrpcResponse, None, None]:
                for response in self.service.getCurrentStates(request, None):
                    yield response

            return [process]

        async def client_test():
            ts = Timestamp()
            ts.FromDatetime(datetime.now())
            request = GetCurrentStatesRequest(messageId=1, fromTimestamp=ts, toTimestamp=ts)

            responses = [response async for response in self.stub.getCurrentStates(request)]

            expected_result = [event for batch in self.current_state_events for event in batch]
            actual_result = [event for res in responses for event in res.event]

            from_timestamp, to_timestamp = self.on_get_current_states.call_args_list[0].args
            assert from_timestamp == request.fromTimestamp.ToDatetime()
            assert to_timestamp == request.toTimestamp.ToDatetime()
            assert [a.messageId for a in responses] == [1, 1, 1]
            assert [a.eventId for a in actual_result] == [e.event_id for e in expected_result]
            assert [a.timestamp for a in actual_result] == [
                Timestamp(seconds=int(e.timestamp.replace(tzinfo=timezone.utc).timestamp()), nanos=e.timestamp.microsecond * 1000) for e in expected_result]
            assert [a.switch.mRID for a in actual_result] == [e.mRID for e in expected_result]
            assert [a.switch.action for a in actual_result] == [e.action.value for e in expected_result]
            assert [a.switch.phases for a in actual_result] == [e.phases.value[0] for e in expected_result]

            self.on_get_current_states.assert_called_once()

        await self.mock_server.validate(client_test, [StreamGrpc('getCurrentStates', call_service())])
