#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from collections.abc import AsyncGenerator
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

import grpc
import pytest
from grpc.aio import AioRpcError
from zepben.protobuf.ns.network_state_pb2_grpc import QueryNetworkStateServiceStub, add_QueryNetworkStateServiceServicer_to_server
from zepben.protobuf.ns.network_state_requests_pb2 import GetCurrentStatesRequest
from zepben.protobuf.ns.network_state_responses_pb2 import GetCurrentStatesResponse, SetCurrentStatesResponse

from util import grpc_aio_server
from zepben.evolve import datetime_to_timestamp, SwitchStateEvent, SwitchAction, QueryNetworkStateService, PhaseCode, CurrentStateEventBatch, \
    SetCurrentStatesStatus, BatchNotProcessed, BatchSuccessful


class TestQueryNetworkStateService:
    from_datetime = datetime.now()
    to_datetime = datetime.now() + timedelta(days=1)
    events = [
        SwitchStateEvent("event1", datetime.now(), "mrid1", SwitchAction.OPEN, PhaseCode.ABC),
        SwitchStateEvent("event2", datetime.now(), "mrid1", SwitchAction.CLOSE, PhaseCode.ABN),
        SwitchStateEvent("event3", datetime.now(), "mrid2", SwitchAction.CLOSE, PhaseCode.A)
    ]
    batches = [
        CurrentStateEventBatch(1, [events[0], events[1]]),
        CurrentStateEventBatch(1, [events[1], events[2]])
    ]
    error = RuntimeError("TEST ERROR!")

    @pytest.fixture
    def capture_statuses(self) -> List[SetCurrentStatesStatus]:
        return []

    @pytest.fixture
    def capture_errors(self) -> List[Tuple[str, Optional[Exception]]]:
        return []

    @pytest.fixture
    def on_get_current_states_error(self) -> Optional[Exception]:
        return None

    @pytest.fixture
    def on_report_current_states_error(self) -> Optional[Exception]:
        return None

    @pytest.fixture
    async def grpc_stub(self, capture_statuses, capture_errors, on_get_current_states_error, on_report_current_states_error):
        # Callbacks for the constructor.

        async def on_get_current_states(from_datetime: datetime, to_datetime: datetime) -> AsyncGenerator[CurrentStateEventBatch, None]:
            if on_get_current_states_error:
                raise on_get_current_states_error

            assert from_datetime == self.from_datetime
            assert to_datetime == self.to_datetime

            for event in self.batches:
                yield event

        def on_current_states_status(status: SetCurrentStatesStatus) -> None:
            if on_report_current_states_error:
                raise on_report_current_states_error
            capture_statuses.append(status)

        def on_processing_error(error: str, exception: Optional[Exception]) -> None:
            capture_errors.append((error, exception))

        # End callbacks for the constructor.

        server, host = grpc_aio_server()
        add_QueryNetworkStateServiceServicer_to_server(QueryNetworkStateService(on_get_current_states, on_current_states_status, on_processing_error), server)

        await server.start()
        async with grpc.aio.insecure_channel(host) as channel:
            yield QueryNetworkStateServiceStub(channel)

        await server.stop(None)

    @pytest.mark.asyncio
    async def test_get_current_states(self, grpc_stub):
        request = GetCurrentStatesRequest(
            messageId=1,
            fromTimestamp=datetime_to_timestamp(self.from_datetime),
            toTimestamp=datetime_to_timestamp(self.to_datetime)
        )
        responses = [response async for response in grpc_stub.getCurrentStates(request)]

        def validate(response: GetCurrentStatesResponse, expected_batch: CurrentStateEventBatch):
            assert response.messageId == expected_batch.batch_id

            assert [it.eventId for it in response.event] == [it.event_id for it in expected_batch.events]
            assert [it.timestamp for it in response.event] == [datetime_to_timestamp(it.timestamp) for it in expected_batch.events]

            expected_switch_events = [it for it in expected_batch.events if isinstance(it, SwitchStateEvent)]
            assert [it.switch.mRID for it in response.event] == [it.mrid for it in expected_switch_events]
            # Compare the int version in the response with the value of the SwitchAction enum.
            assert [it.switch.action for it in response.event] == [it.action.value for it in expected_switch_events]
            # Compare the int version in the response with the first value of the PhaseCode enum (it has multiple values).
            assert [it.switch.phases for it in response.event] == [it.phases.value[0] for it in expected_switch_events]

        assert len(responses) == len(self.batches)
        for index, response in enumerate(responses):
            validate(response, self.batches[index])

    # noinspection PyTestParametrized
    @pytest.mark.asyncio
    @pytest.mark.parametrize('on_get_current_states_error', [error])
    async def test_get_current_states_handles_error(self, grpc_stub):
        with pytest.raises(AioRpcError) as e_info:
            # noinspection PyUnusedLocal
            responses = [response async for response in grpc_stub.getCurrentStates(GetCurrentStatesRequest())]

        assert e_info.value.code() == grpc.StatusCode.UNKNOWN
        assert str(self.error) in str(e_info.value)

    @pytest.mark.asyncio
    async def test_can_receive_status_responses(self, grpc_stub, capture_statuses):
        # The requests for this call are actually response objects (deliberately).
        requests = [BatchNotProcessed(1).to_pb(), BatchSuccessful(2).to_pb()]
        await grpc_stub.reportBatchStatus(requests)

        assert [it.batch_id for it in capture_statuses] == [1, 2]
        assert [type(it) for it in capture_statuses] == [BatchNotProcessed, BatchSuccessful]

    @pytest.mark.asyncio
    async def test_calls_process_error_handler_with_unknown_status_responses(self, grpc_stub, capture_errors):
        # The requests for this call are actually response objects (deliberately).
        # Not sure if/how we can set this to something not supported like you would get from a future version, so just leave it blank.
        requests = [SetCurrentStatesResponse(messageId=1)]
        await grpc_stub.reportBatchStatus(requests)

        assert capture_errors == [("Failed to decode status response for batch `1`: Unsupported type None", None)]

    # noinspection PyTestParametrized
    @pytest.mark.asyncio
    @pytest.mark.parametrize('on_report_current_states_error', [error])
    async def test_calls_process_error_handler_with_exception_in_status_handler(self, grpc_stub, capture_errors):
        requests = [BatchSuccessful(1).to_pb()]
        await grpc_stub.reportBatchStatus(requests)

        assert capture_errors == [(f"Exception thrown in status response handler for batch `1`: {self.error}", self.error)]
