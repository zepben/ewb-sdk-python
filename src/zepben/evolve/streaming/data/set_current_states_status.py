#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["SetCurrentStatesStatus", "BatchSuccessful", "BatchFailure", "BatchNotProcessed", "StateEventFailure", "StateEventInvalidMrid",
           "StateEventUnknownMrid", "StateEventDuplicateMrid", "StateEventUnsupportedPhasing", "StateEventUnsupportedMrid"]

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Tuple, Any

from zepben.protobuf.ns.data.change_status_pb2 import BatchSuccessful as PBBatchSuccessful, BatchFailure as PBBatchFailure, \
    BatchNotProcessed as PBBatchNotProcessed, StateEventFailure as PBStateEventFailure, StateEventUnknownMrid as PBStateEventUnknownMrid, \
    StateEventDuplicateMrid as PBStateEventDuplicateMrid, StateEventInvalidMrid as PBStateEventInvalidMrid, \
    StateEventUnsupportedPhasing as PBStateEventUnsupportedPhasing, StateEventUnsupportedMrid as PBStateEventUnsupportedMrid
from zepben.protobuf.ns.network_state_responses_pb2 import SetCurrentStatesResponse as PBSetCurrentStatesResponse


class SetCurrentStatesStatus(ABC):
    """
    The outcome of processing this batch of updates.

    Attributes:
        batch_id: The unique identifier of the batch that was processed. This matches the
                  batch ID from the original request to allow correlation between request and response.
    """

    def __init__(self, batch_id: int):
        self.batch_id = batch_id

    @staticmethod
    def from_pb(pb: PBSetCurrentStatesResponse) -> 'SetCurrentStatesStatus':
        """
        Creates a BatchSuccessful object from a protobuf SetCurrentStatesResponse.
        """
        status = pb.WhichOneof("status")
        if status == "success":
            return BatchSuccessful.from_pb(pb)
        elif status == "failure":
            return BatchFailure.from_pb(pb)
        elif status == "notProcessed":
            return BatchNotProcessed.from_pb(pb)

    @abstractmethod
    def to_pb(self) -> PBSetCurrentStatesResponse:
        """
        Creates a protobuf SetCurrentStatesResponse object with status.
        """
        pass


@dataclass
class BatchSuccessful(SetCurrentStatesStatus):
    """
    A response indicating all items in the batch were applied successfully.

    Attributes:
        batch_id: The unique identifier of the batch that was processed. This matches the
                  batch ID from the original request to allow correlation between request and response.
    """

    def __init__(self, batch_id: int):
        super().__init__(batch_id)

    @staticmethod
    def from_pb(pb: PBSetCurrentStatesResponse) -> 'BatchSuccessful':
        """
        Creates a BatchSuccessful object from a protobuf SetCurrentStatesResponse.
        """
        return BatchSuccessful(batch_id=pb.messageId)

    def to_pb(self) -> PBSetCurrentStatesResponse:
        """
        Creates a protobuf SetCurrentStatesResponse object with success.
        """
        return PBSetCurrentStatesResponse(messageId=self.batch_id, success=PBBatchSuccessful())


@dataclass
class BatchFailure(SetCurrentStatesStatus):
    """
    A response indicating one or more items in the batch couldn't be applied.

    Attributes:
        batch_id: The unique identifier of the batch that was processed. This matches the
                  batch ID from the original request to allow correlation between request and response.
        partial_failure: Indicates if only some of the batch failed (True), or all entries in the batch failed (False).
        failures: The status of each item processed in the batch that failed.
    """

    def __init__(self, batch_id: int, partial_failure: bool, failures: Tuple['StateEventFailure', Any]):
        super().__init__(batch_id)
        self.partial_failure = partial_failure
        self.failures = failures

    @staticmethod
    def from_pb(pb: PBSetCurrentStatesResponse) -> 'BatchFailure':
        """
        Creates a BatchFailure object from a protobuf SetCurrentStatesResponse.
        """
        failures: List['StateEventFailure'] = []
        for fail in pb.failure.failed:
            event_failure = StateEventFailure.from_pb(fail)
            if event_failure is not None:
                failures.append(event_failure)

        return BatchFailure(batch_id=pb.messageId, partial_failure=pb.failure.partialFailure, failures=tuple(failures))

    def to_pb(self) -> PBSetCurrentStatesResponse:
        """
        Creates a protobuf SetCurrentStatesResponse object with failure.
        """
        return PBSetCurrentStatesResponse(messageId=self.batch_id,
                                          failure=PBBatchFailure(partialFailure=self.partial_failure, failed=[fail.to_pb() for fail in self.failures]))


@dataclass
class BatchNotProcessed(SetCurrentStatesStatus):
    """
    A response indicating all items in the batch were ignored because the message ID of the batch was prior to the
    last processed batch. This is expected when starting the service if the same item is sent to the current state
    processing queue and is also included in the backlog processing response.

    Attributes:
        batch_id: The unique identifier of the batch that was processed. This matches the
                  batch ID from the original request to allow correlation between request and response.
    """

    def __init__(self, batch_id: int):
        super().__init__(batch_id)

    @staticmethod
    def from_pb(pb: PBSetCurrentStatesResponse) -> 'BatchNotProcessed':
        """
        Creates a BatchNotProcessed object from a protobuf SetCurrentStatesResponse.
        """
        return BatchNotProcessed(batch_id=pb.messageId)

    def to_pb(self) -> PBSetCurrentStatesResponse:
        """
        Creates a protobuf SetCurrentStatesResponse object with notProcessed.
        """
        return PBSetCurrentStatesResponse(messageId=self.batch_id, notProcessed=PBBatchNotProcessed())


class StateEventFailure(ABC):
    """
    A wrapper class for allowing a one-of to be repeated.

    Attributes:
        event_id: The event ID of the state event that failed.
        message: A message describing why the event failed.
    """

    def __init__(self, event_id: str, message: str):
        self.event_id = event_id
        self.message = message

    @staticmethod
    def from_pb(pb: PBStateEventFailure) -> Optional['StateEventFailure']:
        """
        Creates a StateEventFailure object from a protobuf StateEventFailure.
        """
        reason_code = pb.WhichOneof('reason')
        if reason_code == "unknownMrid":
            return StateEventUnknownMrid.from_pb(pb)
        elif reason_code == "duplicateMrid":
            return StateEventDuplicateMrid.from_pb(pb)
        elif reason_code == "invalidMrid":
            return StateEventInvalidMrid.from_pb(pb)
        elif reason_code == "unsupportedPhasing":
            return StateEventUnsupportedPhasing.from_pb(pb)
        elif reason_code == "unsupportedMrid":
            return StateEventUnsupportedMrid.from_pb(pb)
        else:
            return None

    @abstractmethod
    def to_pb(self) -> PBStateEventFailure:
        """
        Creates a protobuf StateEventFailure of the appropriate type.
        """
        pass


class StateEventUnknownMrid(StateEventFailure):
    """
    The requested mRID was not found in the network.
    """

    @staticmethod
    def from_pb(pb: PBStateEventFailure) -> 'StateEventUnknownMrid':
        """
        Creates a StateEventUnknownMrid object from a protobuf StateEventFailure.
        """
        return StateEventUnknownMrid(pb.eventId, pb.message)

    def to_pb(self) -> PBStateEventFailure:
        return PBStateEventFailure(
            eventId=self.event_id,
            message=self.message,
            unknownMrid=PBStateEventUnknownMrid()
        )


class StateEventDuplicateMrid(StateEventFailure):
    """
    The requested mRID already existed in the network and can't be used.
    """

    @staticmethod
    def from_pb(pb: PBStateEventFailure) -> 'StateEventDuplicateMrid':
        """
        Creates a StateEventDuplicateMrid object from a protobuf StateEventFailure.
        """
        return StateEventDuplicateMrid(pb.eventId, pb.message)

    def to_pb(self) -> PBStateEventFailure:
        return PBStateEventFailure(
            eventId=self.event_id,
            message=self.message,
            duplicateMrid=PBStateEventDuplicateMrid()
        )


class StateEventInvalidMrid(StateEventFailure):
    """
    The requested mRID was found in the network model, but was of an invalid type.
    """

    @staticmethod
    def from_pb(pb: PBStateEventFailure) -> 'StateEventInvalidMrid':
        """
        Creates a StateEventInvalidMrid object from a protobuf StateEventFailure.
        """
        return StateEventInvalidMrid(pb.eventId, pb.message)

    def to_pb(self) -> PBStateEventFailure:
        return PBStateEventFailure(
            eventId=self.event_id,
            message=self.message,
            invalidMrid=PBStateEventInvalidMrid()
        )


class StateEventUnsupportedPhasing(StateEventFailure):
    """
    The requested phasing was not available for the given operation. For example, an open state request was made with
    unsupported phases.
    """

    @staticmethod
    def from_pb(pb: PBStateEventFailure) -> 'StateEventUnsupportedPhasing':
        """
        Creates a StateEventUnsupportedPhasing object from a protobuf StateEventFailure.
        """
        return StateEventUnsupportedPhasing(pb.eventId, pb.message)

    def to_pb(self) -> PBStateEventFailure:
        return PBStateEventFailure(
            eventId=self.event_id,
            message=self.message,
            unsupportedPhasing=PBStateEventUnsupportedPhasing()
        )


class StateEventUnsupportedMrid(StateEventFailure):
    """
    The mRID provided can't be used to perform the given action even though it is of the correct type. e.g. Trying to
    open/close a switch in a voltage level that hasn't been implemented in the server.
    """

    @staticmethod
    def from_pb(pb: PBStateEventFailure) -> 'StateEventUnsupportedMrid':
        """
        Creates a StateEventUnsupportedMrid object from a protobuf StateEventFailure.
        """
        return StateEventUnsupportedMrid(pb.eventId, pb.message)

    def to_pb(self) -> PBStateEventFailure:
        return PBStateEventFailure(
            eventId=self.event_id,
            message=self.message,
            unsupportedMrid=PBStateEventUnsupportedMrid()
        )
