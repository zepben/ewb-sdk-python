#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.protobuf.ns.data.change_status_pb2 import StateEventFailure as PBStateEventFailure, StateEventInvalidMrid as PBStateEventInvalidMrid

from zepben.evolve import BatchSuccessful, BatchFailure, StateEventInvalidMrid, StateEventFailure, \
    StateEventUnknownMrid, StateEventDuplicateMrid, StateEventUnsupportedPhasing, SetCurrentStatesStatus, BatchNotProcessed
from zepben.evolve.streaming.data.set_current_states_status import StateEventUnsupportedMrid


class TestSetCurrentStatesStatus:
    invalid_mrid = PBStateEventFailure(eventId="event2", invalidMrid=PBStateEventInvalidMrid())

    #
    # NOTE: We don't bother to check that the correct thing was put into the protobuf variants directly because it is
    #       assumed that if the resulting object coming out the other side is correct then the intermediate one must
    #       have been correct (good enough for us anyway).
    #

    def test_batch_successful_to_and_from_protobuf(self):
        original = BatchSuccessful(1)
        converted = SetCurrentStatesStatus.from_pb(original.to_pb())

        assert isinstance(converted, type(original))
        assert converted.batch_id == original.batch_id

    def test_batch_failure_to_and_from_protobuf(self):
        original = BatchFailure(1, True, (StateEventInvalidMrid("event1", "message1"), StateEventUnsupportedMrid("event2", "message2")))
        converted = SetCurrentStatesStatus.from_pb(original.to_pb())

        assert isinstance(converted, type(original))
        assert converted.batch_id == original.batch_id
        assert converted.partial_failure == original.partial_failure

        assert [type(it) for it in converted.failures] == [StateEventInvalidMrid, StateEventUnsupportedMrid]
        assert [it.event_id for it in converted.failures] == ["event1", "event2"]
        assert [it.message for it in converted.failures] == ["message1", "message2"]

    def test_batch_not_processed_to_and_from_protobuf(self):
        original = BatchNotProcessed(1)
        converted = SetCurrentStatesStatus.from_pb(original.to_pb())

        assert isinstance(converted, type(original))
        assert converted.batch_id == original.batch_id

    def test_state_event_failures_to_and_from_protobuf(self):
        self._test_state_event_failure(StateEventUnknownMrid("event1", "unknown mrid message"))
        self._test_state_event_failure(StateEventInvalidMrid("event2", "invalid mrid message"))
        self._test_state_event_failure(StateEventDuplicateMrid("event3", "duplicate mrid message"))
        self._test_state_event_failure(StateEventUnsupportedPhasing("event4", "unsupported phasing message"))
        self._test_state_event_failure(StateEventUnsupportedMrid("event5", "unsupported mrid message"))

        # Unknown protobuf types return None.
        assert StateEventFailure.from_pb(PBStateEventFailure()) is None

    @staticmethod
    def _test_state_event_failure(original: StateEventFailure):
        converted = StateEventFailure.from_pb(original.to_pb())

        assert isinstance(converted, type(original))
        assert converted.event_id == original.event_id
        assert converted.message == original.message
