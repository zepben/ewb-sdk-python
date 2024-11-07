#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Tuple
from abc import ABC, abstractmethod

from zepben.protobuf.ns.data.change_status_pb2 import BatchSuccessful as PBBatchSuccessful, ProcessingPaused as PBProcessingPaused, \
    BatchFailure as PBBatchFailure, StateEventFailure as PBStateEventFailure, StateEventUnknownMrid as PBStateEventUnknownMrid, \
    StateEventDuplicateMrid as PBStateEventDuplicateMrid, StateEventInvalidMrid as PBStateEventInvalidMrid, \
    StateEventUnsupportedPhasing as PBStateEventUnsupportedPhasing

from zepben.evolve import datetime_to_timestamp


class SetCurrentStatesStatus(ABC):
    pass

@dataclass
class BatchSuccessful(SetCurrentStatesStatus):

    @staticmethod
    def from_pb(pb: PBBatchSuccessful) -> 'BatchSuccessful':
        return BatchSuccessful()

    def to_pb(self) -> PBBatchSuccessful:
        return PBBatchSuccessful()

@dataclass
class ProcessingPaused(SetCurrentStatesStatus):

    def __init__(self, since: datetime):
        self.since = since

    @staticmethod
    def from_pb(pb: PBProcessingPaused) -> 'ProcessingPaused':
        return ProcessingPaused(pb.since.ToDatetime())

    def to_pb(self) -> PBProcessingPaused:
        return PBProcessingPaused(since=datetime_to_timestamp(self.since))

@dataclass
class BatchFailure(SetCurrentStatesStatus):

    def __init__(self, partial_failure: bool, failures: Tuple['StateEventFailure', ...]):
        self.partial_failure = partial_failure
        self.failures = failures

    @staticmethod
    def from_pb(pb: PBBatchFailure) -> 'BatchFailure':
        failures: List['StateEventFailure'] = []
        for fail in pb.failed:
            event_failure = StateEventFailure.from_pb(fail)
            if event_failure is not None:
                failures.append(event_failure)

        return BatchFailure(pb.partialFailure, tuple(failures))

    def to_pb(self) -> PBBatchFailure:
        return PBBatchFailure(partialFailure=self.partial_failure, failed=[fail.to_pb() for fail in self.failures])


class StateEventFailure(ABC):

    def __init__(self, event_id: str):
        self.event_id = event_id

    @staticmethod
    def from_pb(pb: PBStateEventFailure) -> Optional['StateEventFailure']:
        reason_code = pb.WhichOneof('reason')
        if reason_code == "unknownMrid":
            return StateEventUnknownMrid.from_pb(pb)
        elif reason_code == "duplicateMrid":
            return StateEventDuplicateMrid.from_pb(pb)
        elif reason_code == "invalidMrid":
            return StateEventInvalidMrid.from_pb(pb)
        elif reason_code == "unsupportedPhasing":
            return StateEventUnsupportedPhasing.from_pb(pb)
        else:
            return None

    @abstractmethod
    def to_pb(self) -> PBStateEventFailure:
        pass


class StateEventUnknownMrid(StateEventFailure):

    @staticmethod
    def from_pb(pb: PBStateEventFailure) -> 'StateEventUnknownMrid':
        return StateEventUnknownMrid(pb.eventId)

    def to_pb(self) -> PBStateEventFailure:
        return PBStateEventFailure(eventId=self.event_id, unknownMrid=PBStateEventUnknownMrid())


class StateEventDuplicateMrid(StateEventFailure):

    @staticmethod
    def from_pb(pb: PBStateEventFailure) -> 'StateEventDuplicateMrid':
        return StateEventDuplicateMrid(pb.eventId)

    def to_pb(self) -> PBStateEventFailure:
        return PBStateEventFailure(eventId=self.event_id, duplicateMrid=PBStateEventDuplicateMrid())


class StateEventInvalidMrid(StateEventFailure):

    @staticmethod
    def from_pb(pb: PBStateEventFailure) -> 'StateEventInvalidMrid':
        return StateEventInvalidMrid(pb.eventId)

    def to_pb(self) -> PBStateEventFailure:
        return PBStateEventFailure(eventId=self.event_id, invalidMrid=PBStateEventInvalidMrid())


class StateEventUnsupportedPhasing(StateEventFailure):

    @staticmethod
    def from_pb(pb: PBStateEventFailure) -> 'StateEventUnsupportedPhasing':
        return StateEventUnsupportedPhasing(pb.eventId)

    def to_pb(self) -> PBStateEventFailure:
        return PBStateEventFailure(eventId=self.event_id, unsupportedPhasing=PBStateEventUnsupportedPhasing())
