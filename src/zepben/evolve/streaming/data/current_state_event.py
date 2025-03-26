#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["CurrentStateEvent", "SwitchStateEvent", "SwitchAction", "AddCutEvent", "RemoveCutEvent", "AddJumperEvent", "RemoveJumperEvent", "JumperConnection"]

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from zepben.protobuf.ns.data.change_events_pb2 import CurrentStateEvent as PBCurrentStateEvent, SwitchStateEvent as PBSwitchStateEvent, \
    AddCutEvent as PBAddCutEvent, RemoveCutEvent as PBRemoveCutEvent, AddJumperEvent as PBAddJumperEvent, RemoveJumperEvent as PBRemoveJumperEvent, \
    JumperConnection as PBJumperConnection

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
        Creates a `CurrentStateEvent` object from a protobuf `CurrentStateEvent`.
        """
        active_event = event.WhichOneof("event")
        if active_event == "switch":
            return SwitchStateEvent.from_pb(event)
        elif active_event == "addCut":
            return AddCutEvent.from_pb(event)
        elif active_event == "removeCut":
            return RemoveCutEvent.from_pb(event)
        elif active_event == "addJumper":
            return AddJumperEvent.from_pb(event)
        elif active_event == "removeJumper":
            return RemoveJumperEvent.from_pb(event)
        else:
            raise NotImplementedError(f"'{active_event}' is currently unsupported.")

    @abstractmethod
    def to_pb(self) -> PBCurrentStateEvent:
        """
        Creates a protobuf `CurrentStateEvent` object with switch from this `CurrentStateEvent`.
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
        Creates a `SwitchStateEvent` object from a protobuf `CurrentStateEvent`.
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
        Creates a protobuf `CurrentStateEvent` object with `switch` from this `SwitchStateEvent`.
        """
        return PBCurrentStateEvent(
            eventId=self.event_id,
            timestamp=datetime_to_timestamp(self.timestamp),
            switch=PBSwitchStateEvent(mRID=self.mrid, action=self.action.name, phases=self.phases.name)
        )


@dataclass
class AddCutEvent(CurrentStateEvent):
    """
    An event to add a cut to the network.

    Attributes:
        event_id: An identifier of this event. This must be unique across requests to allow detection of
          duplicates when requesting events via dates vs those streamed via live updates.
        timestamp: The timestamp when the event occurred. This is always handled as UTC (Coordinated Universal Time).
        mrid: The mRID of the cut defined by this event. This should match any future remove instructions.
        acls_mrid: The mRID of the AC line segment that was cut.
    """

    def __init__(self, event_id: str, timestamp: datetime, mrid: str, acls_mrid: str):
        super().__init__(event_id, timestamp)
        self.mrid = mrid
        self.acls_mrid = acls_mrid

    @staticmethod
    def from_pb(event: PBCurrentStateEvent) -> 'AddCutEvent':
        """
        Creates an `AddCutEvent` object from a protobuf `PBCurrentStateEvent`
        """
        return AddCutEvent(
            event.eventId,
            event.timestamp.ToDatetime(),
            event.addCut.mRID,
            event.addCut.aclsMRID
        )

    def to_pb(self) -> PBCurrentStateEvent:
        """
        Creates a protobuf `PBCurrentStateEvent` object with `addCut` from this `AddCutEvent`
        """
        return PBCurrentStateEvent(
            eventId=self.event_id,
            timestamp=datetime_to_timestamp(self.timestamp),
            addCut=PBAddCutEvent(mRID=self.mrid, aclsMRID=self.acls_mrid)
        )


@dataclass
class RemoveCutEvent(CurrentStateEvent):
    """
    An event to remove a cut from the network.

    Attributes:
        event_id: An identifier of this event. This must be unique across requests to allow detection of
          duplicates when requesting events via dates vs those streamed via live updates.
        timestamp: The timestamp when the event occurred. This is always handled as UTC (Coordinated Universal Time).
        mrid: The mRID of the cut to remove. This should match a previously added cut.
    """

    def __init__(self, event_id: str, timestamp: datetime, mrid: str):
        super().__init__(event_id, timestamp)
        self.mrid = mrid

    @staticmethod
    def from_pb(event: PBCurrentStateEvent) -> 'RemoveCutEvent':
        """
        Creates a `RemoveCutEvent` object from protobuf `PBCurrentStateEvent`
        """
        return RemoveCutEvent(
            event.eventId,
            event.timestamp.ToDatetime(),
            event.removeCut.mRID
        )

    def to_pb(self) -> PBCurrentStateEvent:
        """
        Creates a protobuf `PBCurrentStateEvent` object with `removeCut` from this `RemoveCutEvent`
        """
        return PBCurrentStateEvent(
            eventId=self.event_id,
            timestamp=datetime_to_timestamp(self.timestamp),
            removeCut=PBRemoveCutEvent(mRID=self.mrid)
        )


@dataclass
class AddJumperEvent(CurrentStateEvent):
    """
    An event to add a jumper to the network.

    Attributes:
        event_id: An identifier of this event. This must be unique across requests to allow detection of
          duplicates when requesting events via dates vs those streamed via live updates.
        timestamp: The timestamp when the event occurred. This is always handled as UTC (Coordinated Universal Time).
        mrid: The mRID of the jumper affected by this event.
        from_connection: Information on how this jumper is connected at one end of the jumper.
        to_connection: Information on how this jumper is connected at the other end of the jumper.
    """

    def __init__(self, event_id: str, timestamp: datetime, mrid: str, from_connection: 'JumperConnection', to_connection: 'JumperConnection'):
        super().__init__(event_id, timestamp)
        self.mrid = mrid
        self.from_connection = from_connection
        self.to_connection = to_connection

    @staticmethod
    def from_pb(event: PBCurrentStateEvent) -> 'AddJumperEvent':
        """
        Creates an `AddJumperEvent` object from protobuf `PBCurrentStateEvent`
        """
        return AddJumperEvent(
            event.eventId,
            event.timestamp.ToDatetime(),
            event.addJumper.mRID,
            JumperConnection.from_pb(event.addJumper.fromConnection),
            JumperConnection.from_pb(event.addJumper.toConnection)
        )

    def to_pb(self) -> PBCurrentStateEvent:
        """
        Creates a protobuf `PBCurrentStateEvent` object with `addJumper` from this `AddJumperEvent`
        """
        return PBCurrentStateEvent(
            eventId=self.event_id,
            timestamp=datetime_to_timestamp(self.timestamp),
            addJumper=PBAddJumperEvent(mRID=self.mrid, fromConnection=self.from_connection.to_pb(), toConnection=self.to_connection.to_pb())
        )


@dataclass
class RemoveJumperEvent(CurrentStateEvent):
    """
    An event to remove a jumper from the network.

    Attributes:
        event_id: An identifier of this event. This must be unique across requests to allow detection of
          duplicates when requesting events via dates vs those streamed via live updates.
        timestamp: The timestamp when the event occurred. This is always handled as UTC (Coordinated Universal Time).
        mrid: The mRID of the jumper to remove. This should match a previously added jumper.
    """

    def __init__(self, event_id: str, timestamp: datetime, mrid: str):
        super().__init__(event_id, timestamp)
        self.mrid = mrid

    @staticmethod
    def from_pb(event: PBCurrentStateEvent) -> 'RemoveJumperEvent':
        """
        Creates a `RemoveJumperEvent` object from protobuf `PBCurrentStateEvent`
        """
        return RemoveJumperEvent(
            event.eventId,
            event.timestamp.ToDatetime(),
            event.removeJumper.mRID
        )

    def to_pb(self) -> PBCurrentStateEvent:
        """
        Creates a protobuf `PBCurrentStateEvent` object with `removeJumper` from this `RemoveJumperEvent`
        """
        return PBCurrentStateEvent(
            eventId=self.event_id,
            timestamp=datetime_to_timestamp(self.timestamp),
            removeJumper=PBRemoveJumperEvent(mRID=self.mrid)
        )


class SwitchAction(Enum):
    """
    Enum representing possible actions for a switch.
    """
    UNKNOWN = 0  # The specified action was unknown, or was not set.
    OPEN = 1  # A request to open a switch.
    CLOSE = 2  # A request to close a switch.


class JumperConnection:
    """
    Information about how a jumper is connected to the network.

    Attributes:
        connected_mrid: The mRID of the conducting equipment (or terminal) connected to this end of the jumper.
    """

    def __init__(self, connected_mrid: str):
        self.connected_mrid = connected_mrid

    @staticmethod
    def from_pb(connection: PBJumperConnection) -> 'JumperConnection':
        """
        Creates a `JumperConnection` object from protobuf `PBJumperConnection`
        """
        return JumperConnection(
            connection.connectedMRID,
        )

    def to_pb(self) -> PBJumperConnection:
        """
        Creates a protobuf `PBJumperConnection` object from this `JumperConnection`
        """
        return PBJumperConnection(
            connectedMRID=self.connected_mrid
        )
