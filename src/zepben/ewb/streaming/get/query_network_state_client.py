#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["QueryNetworkStateClient"]

from datetime import datetime
from typing import List, Callable, AsyncGenerator

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.protobuf.ns.network_state_pb2_grpc import QueryNetworkStateServiceStub
from zepben.protobuf.ns.network_state_requests_pb2 import GetCurrentStatesRequest

from zepben.ewb.streaming.data.current_state_event import CurrentStateEvent
from zepben.ewb.streaming.data.current_state_event_batch import CurrentStateEventBatch
from zepben.ewb.streaming.data.set_current_states_status import SetCurrentStatesStatus
from zepben.ewb.streaming.grpc.grpc import GrpcClient
from zepben.ewb.util import datetime_to_timestamp


@dataslot
class QueryNetworkStateClient(GrpcClient):
    """
    A client class that provides functionality to interact with the gRPC service for querying network states.
    A gRPC channel or stub must be provided.
    """

    _stub: QueryNetworkStateServiceStub = None

    async def get_current_states(self, query_id: int, from_datetime: datetime, to_datetime: datetime) -> AsyncGenerator[CurrentStateEventBatch, None]:
        """
        Asynchronously retrieves a collection containing CurrentStateEvent objects, representing the network states
        within a specified time range.

        Args:
            query_id: A unique identifier for the query being processed.
            from_datetime: The start time, as a datetime, for the query range.
            to_datetime: The end time, as a datetime, for the query range.

        Returns:
            A stream of batched network state events in the specified time range.
        """
        request = GetCurrentStatesRequest(
            messageId=query_id,
            fromTimestamp=datetime_to_timestamp(from_datetime),
            toTimestamp=datetime_to_timestamp(to_datetime)
        )
        async for response in self._stub.getCurrentStates(request):
            yield CurrentStateEventBatch(response.messageId, [CurrentStateEvent.from_pb(event) for event in response.event])

    def report_batch_status(self, status: SetCurrentStatesStatus):
        """
        Send a response to a previous `getCurrentStates` request to let the server know how we handled its response.
        :param status: The batch status to report.
        """
        self._stub.reportBatchStatus(iter([status.to_pb()]))
