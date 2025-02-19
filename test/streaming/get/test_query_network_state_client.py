#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import datetime, timedelta
from typing import List, Callable, Generator

import grpc_testing
import pytest
from google.protobuf import empty_pb2
from zepben.protobuf.ns import network_state_pb2
from zepben.protobuf.ns.network_state_responses_pb2 import GetCurrentStatesResponse

from streaming.get.grpcio_aio_testing.mock_async_channel import async_testing_channel
from streaming.get.mock_server import MockServer, GrpcRequest, GrpcResponse, StreamGrpc, StreamUnaryGrpc
from zepben.evolve import PhaseCode, datetime_to_timestamp, SwitchStateEvent, SwitchAction, CurrentStateEventBatch, QueryNetworkStateClient, BatchSuccessful


def _current_state_batch_to_pb(batch: CurrentStateEventBatch) -> GetCurrentStatesResponse:
    return GetCurrentStatesResponse(messageId=batch.batch_id, event=[event.to_pb() for event in batch.events])


class TestQueryNetworkStateClient:

    @pytest.fixture(autouse=True)
    def setup(self):
        channel = async_testing_channel(network_state_pb2.DESCRIPTOR.services_by_name.values(), grpc_testing.strict_real_time())
        self.mock_server = MockServer(channel, network_state_pb2.DESCRIPTOR.services_by_name['QueryNetworkStateService'])
        self.client = QueryNetworkStateClient(channel)
        self.batches = [
            CurrentStateEventBatch(1, [SwitchStateEvent("event1", datetime.now(), "mrid1", SwitchAction.OPEN, PhaseCode.ABC)]),
            CurrentStateEventBatch(2, [SwitchStateEvent("event2", datetime.now(), "mrid1", SwitchAction.CLOSE, PhaseCode.ABN)]),
            CurrentStateEventBatch(3, [SwitchStateEvent("event3", datetime.now(), "mrid2", SwitchAction.CLOSE, PhaseCode.A)])
        ]

    @pytest.mark.asyncio
    async def test_get_current_states(self, caplog):
        query_id = 1
        from_datetime = datetime.now()
        to_datetime = datetime.now() + timedelta(days=1)
        responses = [_current_state_batch_to_pb(it) for it in self.batches]

        def mock_service() -> List[Callable[[GrpcRequest], Generator[GrpcResponse, None, None]]]:
            def process(request: GrpcRequest) -> Generator[GrpcResponse, None, None]:
                assert request.messageId == query_id
                assert request.fromTimestamp == datetime_to_timestamp(from_datetime)
                assert request.toTimestamp == datetime_to_timestamp(to_datetime)

                for response in responses:
                    yield response

            return [process]

        async def client_test():
            results = [response async for response in self.client.get_current_states(query_id, from_datetime, to_datetime)]
            assert results == self.batches

        await self.mock_server.validate(client_test, [StreamGrpc('getCurrentStates', mock_service())])

    @pytest.mark.asyncio
    async def test_can_report_batch_status(self):
        status = BatchSuccessful(1234)

        def mock_service() -> List[Callable[[GrpcRequest], None]]:
            def validate_request(request: GrpcRequest):
                assert request.messageId == status.batch_id

            return [validate_request]

        async def client_test():
            self.client.report_batch_status(status)

        # noinspection PyUnresolvedReferences
        await self.mock_server.validate(client_test, [StreamUnaryGrpc('reportBatchStatus', mock_service(), empty_pb2.Empty())])
