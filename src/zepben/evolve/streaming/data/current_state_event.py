#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["CurrentStateEvent", "SwitchStateEvent", "SwitchAction"]

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from zepben.protobuf.ns.data.change_events_pb2 import CurrentStateEvent as PBCurrentStateEvent, SwitchStateEvent as PBSwitchStateEvent

from zepben.evolve.model.cim.iec61970.base.core.phase_code import PhaseCode, phase_code_by_id
from zepben.evolve.util import datetime_to_timestamp


@dataclass
class CurrentStateEvent(ABC):
    """
    An event to apply to the current state of the network.

    Attributes:
        event_id: An identifier of this event. This must be unique across requests to allow detection of
                  duplicates when requesting events via dates versus those streamed via live updates.
        timestamp: The timestamp when the event occurred.
    """

    def __init__(self, event_id: str, timestamp: datetime):
        self.event_id = event_id
        self.timestamp = timestamp

    @staticmethod
    def from_pb(event: PBCurrentStateEvent) -> 'CurrentStateEvent':
        """
        Creates a CurrentStateEvent object from a protobuf CurrentStateEvent.
        """
        active_event = event.WhichOneof("event")
        if active_event == "switch":
            return SwitchStateEvent.from_pb(event)
        else:
            raise NotImplementedError(f"'{active_event}' is currently unsupported.")

    @abstractmethod
    def to_pb(self) -> PBCurrentStateEvent:
        """
        Creates a protobuf CurrentStateEvent object with switch from a CurrentStateEvent.
        """
        pass


@dataclass
class SwitchStateEvent(CurrentStateEvent):
    """
    An event to update the state of a switch.

    Attributes:
        event_id: An identifier of this event. This must be unique across requests to allow detection of
                  duplicates when requesting events via dates versus those streamed via live updates.
        timestamp: The timestamp when the event occurred, always in UTC (Coordinated Universal Time).
        mrid: The mRID of the switch affected by this event.
        action: The action to take on the switch for the specified phases.
        phases: The phases affected by this event. Defaults to 'NONE'.
    """

    def __init__(self, event_id: str, timestamp: datetime, mrid: str, action: 'SwitchAction', phases: PhaseCode = PhaseCode.NONE):
        super().__init__(event_id, timestamp)
        self.mrid = mrid
        self.action = action
        self.phases = phases

    @staticmethod
    def from_pb(event: PBCurrentStateEvent) -> 'SwitchStateEvent':
        """
        Creates a SwitchStateEvent object from a protobuf CurrentStateEvent.
        """
        return SwitchStateEvent(
            event.eventId,
            event.timestamp.ToDatetime(),
            event.switch.mRID,
            SwitchAction(event.switch.action),
            phase_code_by_id(event.switch.phases)
        )

    def to_pb(self) -> PBCurrentStateEvent:
        """
        Creates a protobuf CurrentStateEvent object with switch from a SwitchStateEvent.
        """
        return PBCurrentStateEvent(eventId=self.event_id, timestamp=datetime_to_timestamp(self.timestamp),
                                   switch=PBSwitchStateEvent(mRID=self.mrid, action=self.action.name, phases=self.phases.name))


class SwitchAction(Enum):
    """
    Enum representing possible actions for a switch.
    """
    UNKNOWN = 0  # The specified action was unknown, or was not set.
    OPEN = 1  # A request to open a switch.
    CLOSE = 2  # A request to close a switch.
