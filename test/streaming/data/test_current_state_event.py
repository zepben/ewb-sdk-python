#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from datetime import datetime

import pytest
from zepben.protobuf.cim.iec61970.base.core.PhaseCode_pb2 import PhaseCode as PBPhaseCode
from zepben.protobuf.ns.data.change_events_pb2 import CurrentStateEvent as PBCurrentStateEvent, SwitchStateEvent as PBSwitchStateEvent, \
    AddCutEvent as PBAddCutEvent, RemoveCutEvent as PBRemoveCutEvent, AddJumperEvent as PBAddJumperEvent, RemoveJumperEvent as PBRemoveJumperEvent, \
    SwitchAction as PBSwitchAction, JumperConnection as PBJumperConnection

from zepben.evolve import PhaseCode, datetime_to_timestamp, CurrentStateEvent, SwitchStateEvent, SwitchAction, AddCutEvent, RemoveCutEvent, AddJumperEvent, \
    RemoveJumperEvent


class TestCurrentStateEvent:

    def test_from_pb(self):
        event = CurrentStateEvent.from_pb(PBCurrentStateEvent(switch=PBSwitchStateEvent()))
        assert isinstance(event, SwitchStateEvent)

        event = CurrentStateEvent.from_pb(PBCurrentStateEvent(addCut=PBAddCutEvent()))
        assert isinstance(event, AddCutEvent)

        event = CurrentStateEvent.from_pb(PBCurrentStateEvent(removeCut=PBRemoveCutEvent()))
        assert isinstance(event, RemoveCutEvent)

        event = CurrentStateEvent.from_pb(PBCurrentStateEvent(addJumper=PBAddJumperEvent()))
        assert isinstance(event, AddJumperEvent)

        event = CurrentStateEvent.from_pb(PBCurrentStateEvent(removeJumper=PBRemoveJumperEvent()))
        assert isinstance(event, RemoveJumperEvent)

    def test_from_pb_not_implemented(self):
        with pytest.raises(NotImplementedError):
            CurrentStateEvent.from_pb(PBCurrentStateEvent())

    def test_event_protobuf_conversion(self):
        pb_event = PBCurrentStateEvent(
            eventId="event1",
            timestamp=datetime_to_timestamp(datetime.now()),
            switch=PBSwitchStateEvent(mRID="switch-1", action=PBSwitchAction.SWITCH_ACTION_OPEN, phases=PBPhaseCode.PHASE_CODE_ABCN)
        )

        event = SwitchStateEvent.from_pb(pb_event)
        assert event.event_id == pb_event.eventId
        assert event.timestamp == pb_event.timestamp.ToDatetime()
        assert event.mrid == pb_event.switch.mRID
        assert event.action == SwitchAction.OPEN
        assert event.phases == PhaseCode.ABCN

        pb = event.to_pb()
        assert pb.eventId == pb_event.eventId
        assert pb.timestamp == pb_event.timestamp
        assert pb.switch.mRID == pb_event.switch.mRID
        assert pb.switch.action == pb_event.switch.action
        assert pb.switch.phases == pb_event.switch.phases

    def test_add_cut_event_protobuf_conversion(self):
        pb_event = PBCurrentStateEvent(
            eventId="event1",
            timestamp=datetime_to_timestamp(datetime.now()),
            addCut=PBAddCutEvent(mRID="cut-1", aclsMRID="acls-1")
        )

        event = AddCutEvent.from_pb(pb_event)
        assert event.event_id == pb_event.eventId
        assert event.timestamp == pb_event.timestamp.ToDatetime()
        assert event.mrid == pb_event.addCut.mRID
        assert event.acls_mrid == pb_event.addCut.aclsMRID

        pb = event.to_pb()
        assert pb.eventId == pb_event.eventId
        assert pb.timestamp == pb_event.timestamp
        assert pb.addCut.mRID == pb_event.addCut.mRID
        assert pb.addCut.aclsMRID == pb_event.addCut.aclsMRID

    def test_remove_cut_event_protobuf_conversion(self):
        pb_event = PBCurrentStateEvent(
            eventId="event1",
            timestamp=datetime_to_timestamp(datetime.now()),
            removeCut=PBRemoveCutEvent(mRID="cut-1")
        )

        event = RemoveCutEvent.from_pb(pb_event)
        assert event.event_id == pb_event.eventId
        assert event.timestamp == pb_event.timestamp.ToDatetime()
        assert event.mrid == pb_event.removeCut.mRID

        pb = event.to_pb()
        assert pb.eventId == pb_event.eventId
        assert pb.timestamp == pb_event.timestamp
        assert pb.removeCut.mRID == pb_event.removeCut.mRID

    def test_add_jumper_event_protobuf_conversion(self):
        pb_event = PBCurrentStateEvent(
            eventId="event1",
            timestamp=datetime_to_timestamp(datetime.now()),
            addJumper=PBAddJumperEvent(
                mRID="jumper-1",
                fromConnection=PBJumperConnection(connectedMRID="from-id"),
                toConnection=PBJumperConnection(connectedMRID="to-id")
            )
        )

        event = AddJumperEvent.from_pb(pb_event)
        assert event.event_id == pb_event.eventId
        assert event.timestamp == pb_event.timestamp.ToDatetime()
        assert event.mrid == pb_event.addJumper.mRID
        assert event.from_connection.connected_mrid == pb_event.addJumper.fromConnection.connectedMRID
        assert event.to_connection.connected_mrid == pb_event.addJumper.toConnection.connectedMRID

        pb = event.to_pb()
        assert pb.eventId == pb_event.eventId
        assert pb.timestamp == pb_event.timestamp
        assert pb.addJumper.mRID == pb_event.addJumper.mRID
        assert pb.addJumper.fromConnection.connectedMRID == pb_event.addJumper.fromConnection.connectedMRID
        assert pb.addJumper.toConnection.connectedMRID == pb_event.addJumper.toConnection.connectedMRID

    def test_remove_jumper_event_protobuf_conversion(self):
        pb_event = PBCurrentStateEvent(
            eventId="event1",
            timestamp=datetime_to_timestamp(datetime.now()),
            removeJumper=PBRemoveJumperEvent(mRID="jumper-1")
        )

        event = RemoveJumperEvent.from_pb(pb_event)
        assert event.event_id == pb_event.eventId
        assert event.timestamp == pb_event.timestamp.ToDatetime()
        assert event.mrid == pb_event.removeJumper.mRID

        pb = event.to_pb()
        assert pb.eventId == pb_event.eventId
        assert pb.timestamp == pb_event.timestamp
        assert pb.removeJumper.mRID == pb_event.removeJumper.mRID
