#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["QueryNetworkStateService"]

from datetime import datetime
from typing import Callable, AsyncGenerator, Optional

from google.protobuf import empty_pb2
from zepben.protobuf.ns.network_state_pb2_grpc import QueryNetworkStateServiceServicer
from zepben.protobuf.ns.network_state_requests_pb2 import GetCurrentStatesRequest
from zepben.protobuf.ns.network_state_responses_pb2 import GetCurrentStatesResponse, SetCurrentStatesResponse

from zepben.evolve.streaming.data.current_state_event_batch import CurrentStateEventBatch
from zepben.evolve.streaming.data.set_current_states_status import SetCurrentStatesStatus


class QueryNetworkStateService(QueryNetworkStateServiceServicer):
    """
    A service class that provides a simplified interface for retrieving current state events
    via gRPC without exposing the underlying complexity of gRPC mechanisms.

    This class serves as a wrapper around the gRPC-generated service implementation,
    allowing users to interact with it using a more convenient function type.

    Attributes:
        on_get_current_states: An function that retrieves CurrentStateEvent objects within the specified time range.
        on_current_states_status: A callback triggered when the response status of an event returned via `on_get_current_states` is received from the client.
        on_processing_error: A function that takes a message and optional cause. Called when `on_current_states_status` raises an exception, or the
          `SetCurrentStatesResponse` is for an unknown event status.
    """

    def __init__(
        self,
        on_get_current_states: Callable[[datetime, datetime], AsyncGenerator[CurrentStateEventBatch, None]],
        on_current_states_status: Callable[[SetCurrentStatesStatus], None],
        on_processing_error: Callable[[str, Optional[Exception]], None]
    ):
        self.on_get_current_states = on_get_current_states
        self.on_current_states_status = on_current_states_status
        self.on_processing_error = on_processing_error

    async def getCurrentStates(self, request: GetCurrentStatesRequest, context) -> AsyncGenerator[GetCurrentStatesResponse, None]:
        """
        Handles the incoming request for retrieving current state events.

        You shouldn't be calling this method directly, it will be invoked automatically via the gRPC engine. Each
        `GetCurrentStatesRequest` retrieves the corresponding current state events using the `onGetCurrentStates`
        callback function passed in the constructor, and asynchronously returns a `GetCurrentStatesResponse`.

        It acts as a bridge between the gRPC request and the business logic that fetches the current state events.

        Args:
            request: The request object containing parameters for fetching current state events,
              including the time range for the query.
            context: The gRPC context.

        Returns:
           A stream of gRPC response messages
        """
        async for batch in self.on_get_current_states(request.fromTimestamp.ToDatetime(), request.toTimestamp.ToDatetime()):
            yield GetCurrentStatesResponse(messageId=batch.batch_id, event=[event.to_pb() for event in batch.events])

    # noinspection PyUnresolvedReferences
    async def reportBatchStatus(self, status_responses: AsyncGenerator[SetCurrentStatesResponse, None], context) -> empty_pb2.Empty:
        """
        Handles incoming status reports in response to an event batch returned via `getCurrentStates`.

        You shouldn't be calling this method directly, it will be invoked automatically via the gRPC engine. Each
        `SetCurrentStatesResponse` will trigger the `on_current_states_status` callback function passed in the constructor.

        It acts as a bridge between the gRPC request and the business logic that validates/logs the status of event
        handling. Any errors in this handling, or unexpected status message will trigger the `on_processing_error`
        callback function passed in the constructor.

        Args:
            status_responses: The request object stream (yes you read that correctly that the request is a response...) containing the response to our current state batch.
            context: The gRPC context.
        """
        async for status_response in status_responses:
            status = SetCurrentStatesStatus.from_pb(status_response)
            if status is not None:
                try:
                    self.on_current_states_status(status)
                except Exception as e:
                    message = f"Exception thrown in status response handler for batch `{status_response.messageId}`: {str(e)}"
                    self.on_processing_error(message, e)
            else:
                self.on_processing_error(f"Failed to decode status response for batch `{status_response.messageId}`: Unsupported type {status_response.WhichOneof('status')}", None)

        # noinspection PyUnresolvedReferences
        return empty_pb2.Empty()
