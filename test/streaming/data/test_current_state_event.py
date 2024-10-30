#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
from datetime import datetime
from zepben.protobuf.ns.data.change_events_pb2 import CurrentStateEvent as PBCurrentStateEvent, SwitchStateEvent as PBSwitchStateEvent, \
    AddCutEvent as PBAddCutEvent, RemoveCutEvent as PBRemoveCutEvent, AddJumperEvent as PBAddJumperEvent, RemoveJumperEvent as PBRemoveJumperEvent, \
    SwitchAction as PBSwitchAction

from zepben.evolve import PhaseCode
from zepben.evolve.streaming.data.current_state_event import CurrentStateEvent, SwitchStateEvent, SwitchAction
from google.protobuf.timestamp_pb2 import Timestamp as PBTimestamp
from zepben.protobuf.cim.iec61970.base.core.PhaseCode_pb2 import PhaseCode as PBPhaseCode


def _test_from_pb_not_implemented(event: PBCurrentStateEvent):
    with pytest.raises(NotImplementedError):
        CurrentStateEvent._from_pb(event)


class TestCurrentStateEvent:
    def test_from_pb(self):
        switch_event = CurrentStateEvent._from_pb(PBCurrentStateEvent(switch=PBSwitchStateEvent()))
        assert isinstance(switch_event, SwitchStateEvent)

    def test_from_pb_not_implemented(self):
        _test_from_pb_not_implemented(PBCurrentStateEvent(addCut=PBAddCutEvent()))
        _test_from_pb_not_implemented(PBCurrentStateEvent(removeCut=PBRemoveCutEvent()))
        _test_from_pb_not_implemented(PBCurrentStateEvent(addJumper=PBAddJumperEvent()))
        _test_from_pb_not_implemented(PBCurrentStateEvent(removeJumper=PBRemoveJumperEvent()))

    def test_switch_state_event_prtobuf_conversion(self):
        ts = PBTimestamp()
        ts.FromDatetime(datetime.now())
        event = PBCurrentStateEvent(eventId="event1", timestamp=ts,
                                    switch=PBSwitchStateEvent(mRID="switch-1", action=PBSwitchAction.OPEN, phases=PBPhaseCode.ABCN))
        current_state_event = SwitchStateEvent._from_pb(event)
        assert current_state_event.event_id == event.eventId
        assert current_state_event.timestamp == event.timestamp.ToDatetime()
        assert current_state_event.mRID == event.switch.mRID
        assert current_state_event.action == SwitchAction.OPEN
        assert current_state_event.phases == PhaseCode.ABCN

        pb = current_state_event._to_pb()
        assert pb.eventId == event.eventId
        assert pb.timestamp == event.timestamp
        assert pb.switch.mRID == event.switch.mRID
        assert pb.switch.action == event.switch.action
        assert pb.switch.phases == event.switch.phases
