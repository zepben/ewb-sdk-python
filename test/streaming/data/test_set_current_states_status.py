#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import datetime

from zepben.evolve import datetime_to_timestamp
from zepben.evolve.streaming.data.set_current_states_status import BatchSuccessful, ProcessingPaused, BatchFailure, StateEventInvalidMrid, StateEventFailure, \
    StateEventUnknownMrid, StateEventDuplicateMrid, StateEventUnsupportedPhasing, SetCurrentStatesStatus
from zepben.protobuf.ns.data.change_status_pb2 import BatchSuccessful as PBBatchSuccessful, ProcessingPaused as PBProcessingPaused, \
    BatchFailure as PBBatchFailure, StateEventFailure as PBStateEventFailure, StateEventUnknownMrid as PBStateEventUnknownMrid, \
    StateEventDuplicateMrid as PBStateEventDuplicateMrid, StateEventInvalidMrid as PBStateEventInvalidMrid, \
    StateEventUnsupportedPhasing as PBStateEventUnsupportedPhasing
from zepben.protobuf.ns.network_state_responses_pb2 import SetCurrentStatesResponse as PBSetCurrentStatesResponse


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
        pb = PBSetCurrentStatesResponse(messageId=1, success=PBBatchSuccessful())
        status = SetCurrentStatesStatus.from_pb(pb)

        assert status == BatchSuccessful(batch_id=1)
        assert status.to_pb() == pb

    def test_processing_paused_protobuf_conversion(self):
        since = datetime.now()
        pb = PBSetCurrentStatesResponse(messageId=1, paused=PBProcessingPaused(since=datetime_to_timestamp(since)))
        status = SetCurrentStatesStatus.from_pb(pb)

        assert status == ProcessingPaused(batch_id=1, since=since)
        assert status.to_pb() == pb

    def test_batch_failure_protobuf_conversion(self):
        pb = PBSetCurrentStatesResponse(messageId=1, failure=PBBatchFailure(partialFailure=True, failed=[self.invalidMrid]))
        status = SetCurrentStatesStatus.from_pb(pb)

        assert status == BatchFailure(batch_id=1, partial_failure=True, failures=(StateEventInvalidMrid(event_id="event2"),))
        assert status.to_pb() == pb

    def test_state_event_failure_protobuf_conversion(self):
        _test_state_event_failure_protobuf_conversion(PBStateEventFailure(eventId="event1", unknownMrid=PBStateEventUnknownMrid()), StateEventUnknownMrid)
        _test_state_event_failure_protobuf_conversion(self.invalidMrid, StateEventInvalidMrid)
        _test_state_event_failure_protobuf_conversion(PBStateEventFailure(eventId="event3", duplicateMrid=PBStateEventDuplicateMrid()), StateEventDuplicateMrid)
        _test_state_event_failure_protobuf_conversion(
            PBStateEventFailure(eventId="event4", unsupportedPhasing=PBStateEventUnsupportedPhasing()),
            StateEventUnsupportedPhasing)

        assert StateEventFailure.from_pb(PBStateEventFailure()) is None
