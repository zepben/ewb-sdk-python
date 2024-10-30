#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import datetime
from typing import List, Optional, Tuple
from abc import ABC, abstractmethod

from zepben.protobuf.ns.data.change_status_pb2 import BatchSuccessful as PBBatchSuccessful, ProcessingPaused as PBProcessingPaused, \
    BatchFailure as PBBatchFailure, StateEventFailure as PBStateEventFailure, StateEventUnknownMrid as PBStateEventUnknownMrid, \
    StateEventDuplicateMrid as PBStateEventDuplicateMrid, StateEventInvalidMrid as PBStateEventInvalidMrid, \
    StateEventUnsupportedPhasing as PBStateEventUnsupportedPhasing
from .current_state_event import _datetime_to_timestamp


class SetCurrentStatesStatus(ABC):
    pass


class BatchSuccessful(SetCurrentStatesStatus):
    @staticmethod
    def _from_pb(pb: PBBatchSuccessful) -> 'BatchSuccessful':
        return BatchSuccessful()

    def _to_pb(self) -> PBBatchSuccessful:
        return PBBatchSuccessful()


class ProcessingPaused(SetCurrentStatesStatus):
    def __init__(self, since: datetime):
        self.since = since

    @staticmethod
    def _from_pb(pb: PBProcessingPaused) -> 'ProcessingPaused':
        return ProcessingPaused(pb.since.ToDatetime())

    def _to_pb(self) -> PBProcessingPaused:
        return PBProcessingPaused(since=_datetime_to_timestamp(self.since))


class BatchFailure(SetCurrentStatesStatus):
    def __init__(self, partial_failure: bool, failures: Tuple['StateEventFailure', ...]):
        self.partial_failure = partial_failure
        self.failures = failures

    @staticmethod
    def _from_pb(pb: PBBatchFailure) -> 'BatchFailure':
        failures: List['StateEventFailure'] = []
        for fail in pb.failed:
            event_failure = StateEventFailure._from_pb(fail)
            if event_failure is not None:
                failures.append(event_failure)

        return BatchFailure(pb.partialFailure, tuple(failures))

    def _to_pb(self) -> PBBatchFailure:
        return PBBatchFailure(partialFailure=self.partial_failure, failed=[fail._to_pb() for fail in self.failures])


class StateEventFailure(ABC):
    def __init__(self, event_id: str):
        self.event_id = event_id

    @staticmethod
    def _from_pb(pb: PBStateEventFailure) -> Optional['StateEventFailure']:
        reason_code = pb.WhichOneof('reason')
        if reason_code == "unknownMrid":
            return StateEventUnknownMrid._from_pb(pb)
        elif reason_code == "duplicateMrid":
            return StateEventDuplicateMrid._from_pb(pb)
        elif reason_code == "invalidMrid":
            return StateEventInvalidMrid._from_pb(pb)
        elif reason_code == "unsupportedPhasing":
            return StateEventUnsupportedPhasing._from_pb(pb)
        else:
            return None

    @abstractmethod
    def _to_pb(self) -> PBStateEventFailure:
        pass


class StateEventUnknownMrid(StateEventFailure):
    @staticmethod
    def _from_pb(pb: PBStateEventFailure) -> 'StateEventUnknownMrid':
        return StateEventUnknownMrid(pb.eventId)

    def _to_pb(self) -> PBStateEventFailure:
        return PBStateEventFailure(eventId=self.event_id, unknownMrid=PBStateEventUnknownMrid())


class StateEventDuplicateMrid(StateEventFailure):
    @staticmethod
    def _from_pb(pb: PBStateEventFailure) -> 'StateEventDuplicateMrid':
        return StateEventDuplicateMrid(pb.eventId)

    def _to_pb(self) -> PBStateEventFailure:
        return PBStateEventFailure(eventId=self.event_id, duplicateMrid=PBStateEventDuplicateMrid())


class StateEventInvalidMrid(StateEventFailure):
    @staticmethod
    def _from_pb(pb: PBStateEventFailure) -> 'StateEventInvalidMrid':
        return StateEventInvalidMrid(pb.eventId)

    def _to_pb(self) -> PBStateEventFailure:
        return PBStateEventFailure(eventId=self.event_id, invalidMrid=PBStateEventInvalidMrid())


class StateEventUnsupportedPhasing(StateEventFailure):
    @staticmethod
    def _from_pb(pb: PBStateEventFailure) -> 'StateEventUnsupportedPhasing':
        return StateEventUnsupportedPhasing(pb.eventId)

    def _to_pb(self) -> PBStateEventFailure:
        return PBStateEventFailure(eventId=self.event_id, unsupportedPhasing=PBStateEventUnsupportedPhasing())
