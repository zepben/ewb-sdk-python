#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import datetime

from zepben.evolve import datetime_to_timestamp
from zepben.evolve.streaming.data.set_current_states_status import BatchSuccessful, ProcessingPaused, BatchFailure, StateEventInvalidMrid, StateEventFailure, \
    StateEventUnknownMrid, StateEventDuplicateMrid, StateEventUnsupportedPhasing
from zepben.protobuf.ns.data.change_status_pb2 import BatchSuccessful as PBBatchSuccessful, ProcessingPaused as PBProcessingPaused, \
    BatchFailure as PBBatchFailure, StateEventFailure as PBStateEventFailure, StateEventUnknownMrid as PBStateEventUnknownMrid, \
    StateEventDuplicateMrid as PBStateEventDuplicateMrid, StateEventInvalidMrid as PBStateEventInvalidMrid, \
    StateEventUnsupportedPhasing as PBStateEventUnsupportedPhasing


def _test_state_event_failure_protobuf_conversion(pb: PBStateEventFailure, clazz: type):
    status = StateEventFailure.from_pb(pb)
    assert status.event_id == pb.eventId
    assert isinstance(status, clazz)

    # noinspection PyUnresolvedReferences
    to_pb = status.to_pb()
    assert to_pb.eventId == pb.eventId
    assert to_pb.WhichOneof("reason") == pb.WhichOneof("reason")


class TestSetCurrentStatesStatus:
    invalidMrid = PBStateEventFailure(eventId="event2", invalidMrid=PBStateEventInvalidMrid())

    def test_batch_successful_protobuf_conversion(self):
        status = BatchSuccessful.from_pb(PBBatchSuccessful())

        assert isinstance(status, BatchSuccessful)
        assert isinstance(status.to_pb(), PBBatchSuccessful)

    def test_processing_paused_protobuf_conversion(self):
        pb = PBProcessingPaused(since=datetime_to_timestamp(datetime.now()))
        status = ProcessingPaused.from_pb(pb)

        assert status.since == pb.since.ToDatetime()
        assert status.to_pb().since == pb.since

    def test_batch_failure_protobuf_conversion(self):
        pb = PBBatchFailure(partialFailure=True, failed=[self.invalidMrid])
        status = BatchFailure.from_pb(pb)

        assert status.partial_failure == pb.partialFailure
        assert len(status.failures) == 1
        assert isinstance(status.failures[0], StateEventInvalidMrid)

        to_pb = status.to_pb()
        assert to_pb.partialFailure == pb.partialFailure
        assert len(to_pb.failed) == 1
        assert to_pb.failed[0].WhichOneof("reason") == "invalidMrid"

    def test_state_event_failure_protobuf_conversion(self):
        _test_state_event_failure_protobuf_conversion(PBStateEventFailure(eventId="event1", unknownMrid=PBStateEventUnknownMrid()), StateEventUnknownMrid)
        _test_state_event_failure_protobuf_conversion(self.invalidMrid, StateEventInvalidMrid)
        _test_state_event_failure_protobuf_conversion(PBStateEventFailure(eventId="event3", duplicateMrid=PBStateEventDuplicateMrid()), StateEventDuplicateMrid)
        _test_state_event_failure_protobuf_conversion(
            PBStateEventFailure(eventId="event4", unsupportedPhasing=PBStateEventUnsupportedPhasing()),
            StateEventUnsupportedPhasing)

        assert StateEventFailure.from_pb(PBStateEventFailure()) is None
