#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from datetime import datetime

import pytest
from zepben.protobuf.cim.iec61970.base.core.PhaseCode_pb2 import PhaseCode as PBPhaseCode
from zepben.protobuf.ns.data.change_events_pb2 import CurrentStateEvent as PBCurrentStateEvent, SwitchStateEvent as PBSwitchStateEvent, \
    AddCutEvent as PBAddCutEvent, RemoveCutEvent as PBRemoveCutEvent, AddJumperEvent as PBAddJumperEvent, RemoveJumperEvent as PBRemoveJumperEvent, \
    SwitchAction as PBSwitchAction

from zepben.evolve import PhaseCode, datetime_to_timestamp, CurrentStateEvent, SwitchStateEvent, SwitchAction


def _test_from_pb_not_implemented(event: PBCurrentStateEvent):
    with pytest.raises(NotImplementedError):
        CurrentStateEvent.from_pb(event)


class TestCurrentStateEvent:

    def test_from_pb(self):
        switch_event = CurrentStateEvent.from_pb(PBCurrentStateEvent(switch=PBSwitchStateEvent()))
        assert isinstance(switch_event, SwitchStateEvent)

    def test_from_pb_not_implemented(self):
        _test_from_pb_not_implemented(PBCurrentStateEvent(addCut=PBAddCutEvent()))
        _test_from_pb_not_implemented(PBCurrentStateEvent(removeCut=PBRemoveCutEvent()))
        _test_from_pb_not_implemented(PBCurrentStateEvent(addJumper=PBAddJumperEvent()))
        _test_from_pb_not_implemented(PBCurrentStateEvent(removeJumper=PBRemoveJumperEvent()))

    def test_switch_state_event_protobuf_conversion(self):
        pb_event = PBCurrentStateEvent(eventId="event1", timestamp=datetime_to_timestamp(datetime.now()),
                                       switch=PBSwitchStateEvent(mRID="switch-1", action=PBSwitchAction.OPEN, phases=PBPhaseCode.ABCN))
        switch_state_event = SwitchStateEvent.from_pb(pb_event)
        assert switch_state_event.event_id == pb_event.eventId
        assert switch_state_event.timestamp == pb_event.timestamp.ToDatetime()
        assert switch_state_event.mrid == pb_event.switch.mRID
        assert switch_state_event.action == SwitchAction.OPEN
        assert switch_state_event.phases == PhaseCode.ABCN

        pb = switch_state_event.to_pb()
        assert pb.eventId == pb_event.eventId
        assert pb.timestamp == pb_event.timestamp
        assert pb.switch.mRID == pb_event.switch.mRID
        assert pb.switch.action == pb_event.switch.action
        assert pb.switch.phases == pb_event.switch.phases
