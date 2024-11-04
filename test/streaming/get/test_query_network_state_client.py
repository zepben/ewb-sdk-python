#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import datetime, timedelta
from typing import List, Callable, Generator, Iterable

import grpc_testing
import pytest
from google.protobuf.timestamp_pb2 import Timestamp
from zepben.protobuf.ns import network_state_pb2
from zepben.protobuf.ns.network_state_pb2_grpc import QueryNetworkStateServiceStub
from zepben.protobuf.ns.network_state_responses_pb2 import GetCurrentStatesResponse

from streaming.get.grpcio_aio_testing.mock_async_channel import async_testing_channel
from streaming.get.mock_server import MockServer, GrpcRequest, GrpcResponse, StreamGrpc
from zepben.evolve import PhaseCode
from zepben.evolve.streaming.data.current_state_event import SwitchStateEvent, SwitchAction
from zepben.evolve.streaming.get.query_network_state_client import QueryNetworkStateClient


class TestQueryNetworkStateClient:

    @pytest.fixture(autouse=True)
    def setup(self):
        channel = async_testing_channel(network_state_pb2.DESCRIPTOR.services_by_name.values(), grpc_testing.strict_real_time())
        self.mock_server = MockServer(channel, network_state_pb2.DESCRIPTOR.services_by_name['QueryNetworkStateService'])
        self.client = QueryNetworkStateClient(stub=QueryNetworkStateServiceStub(channel))

        self.current_state_events = (
            (SwitchStateEvent("event1", datetime.now(), "mrid1", SwitchAction.OPEN, PhaseCode.ABC),),
            (SwitchStateEvent("event2", datetime.now(), "mrid1", SwitchAction.CLOSE, PhaseCode.ABN),),
            (SwitchStateEvent("event3", datetime.now(), "mrid2", SwitchAction.CLOSE, PhaseCode.A),)
        )

    @pytest.mark.asyncio
    async def test_get_current_states(self):
        def mock_service(expected_from_timestamp: datetime, expected_to_timestamp: datetime, responses: Iterable[GrpcResponse]) -> List[
            Callable[[GrpcRequest], Generator[GrpcResponse, None, None]]]:
            def process(request: GrpcRequest) -> Generator[GrpcResponse, None, None]:
                for response in responses:
                    yield response

                assert request.fromTimestamp == expected_from_timestamp
                assert request.toTimestamp == expected_to_timestamp

            return [process]

        async def client_test():
            results = [response async for response in self.client.get_current_states(1, from_datetime, to_datetime)]

            expected_result = [event for batch in self.current_state_events for event in batch]
            actual_result = [event for events in results for event in events]

            assert actual_result == expected_result

        from_datetime = datetime.now()
        from_timestamp = Timestamp()
        from_timestamp.FromDatetime(from_datetime)
        to_datetime = datetime.now() + timedelta(days=1)
        to_timestamp = Timestamp()
        to_timestamp.FromDatetime(to_datetime)

        response1 = GetCurrentStatesResponse(messageId=1, event=[event._to_pb() for event in self.current_state_events[0]])
        response2 = GetCurrentStatesResponse(messageId=1, event=[event._to_pb() for event in self.current_state_events[1]])
        response3 = GetCurrentStatesResponse(messageId=1, event=[event._to_pb() for event in self.current_state_events[2]])

        await self.mock_server.validate(client_test, [StreamGrpc('getCurrentStates',
                                                                 mock_service(from_timestamp, to_timestamp, [response1, response2, response3]))])
