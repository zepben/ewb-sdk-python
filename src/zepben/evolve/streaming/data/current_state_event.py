#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from abc import ABC
from enum import Enum
from datetime import datetime
from zepben.protobuf.ns.data.change_events_pb2 import CurrentStateEvent as PBCurrentStateEvent, SwitchStateEvent as PBSwitchStateEvent
from zepben.evolve.model.cim.iec61970.base.core.phase_code import PhaseCode, phase_code_by_id
from google.protobuf.timestamp_pb2 import Timestamp as PBTimestamp


def _datetime_to_timestamp(date_time: datetime) -> PBTimestamp:
    ts = PBTimestamp()
    ts.FromDatetime(date_time)
    return ts


class CurrentStateEvent(ABC):
    def __init__(self, event_id: str, timestamp: datetime = None):
        self.event_id = event_id
        self.timestamp = timestamp

    @staticmethod
    def _from_pb(event: PBCurrentStateEvent) -> 'CurrentStateEvent':
        active_event = event.WhichOneof("event")
        if active_event == "switch":
            return SwitchStateEvent._from_pb(event)
        else:
            raise NotImplementedError(f"'{active_event}' is currently unsupported.")


class SwitchStateEvent(CurrentStateEvent):
    def __init__(self, event_id: str, timestamp: datetime, mRID: str, action: 'SwitchAction', phases: PhaseCode = PhaseCode.NONE):
        super().__init__(event_id, timestamp)
        self.mRID = mRID
        self.action = action
        self.phases = phases

    @staticmethod
    def _from_pb(event: PBCurrentStateEvent) -> 'SwitchStateEvent':
        return SwitchStateEvent(
            event.eventId,
            event.timestamp.ToDatetime(),
            event.switch.mRID,
            SwitchAction(event.switch.action),
            phase_code_by_id(event.switch.phases)
        )

    def _to_pb(self) -> PBCurrentStateEvent:
        return PBCurrentStateEvent(eventId=self.event_id, timestamp=_datetime_to_timestamp(self.timestamp),
                                   switch=PBSwitchStateEvent(mRID=self.mRID, action=self.action.name, phases=self.phases.name))


class SwitchAction(Enum):
    UNKNOWN = 0
    OPEN = 1
    CLOSE = 2
