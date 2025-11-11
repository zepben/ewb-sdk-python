#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from dataclasses import field
from typing import Optional, Generator
from typing import TYPE_CHECKING
from weakref import ref, ReferenceType

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated

from zepben.ewb.dataslot.dataslot import instantiate
from zepben.ewb.model.cim.iec61970.base.core.ac_dc_terminal import AcDcTerminal
from zepben.ewb.model.cim.iec61970.base.core.feeder import Feeder
from zepben.ewb.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.ewb.model.cim.iec61970.base.wires.busbar_section import BusbarSection
from zepben.ewb.model.phases import TracedPhases
from zepben.ewb.services.network.tracing.feeder.feeder_direction import FeederDirection
from zepben.ewb.services.network.tracing.phases.phase_status import PhaseStatus, NormalPhases, CurrentPhases

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
    from zepben.ewb.model.cim.iec61970.base.core.connectivity_node import ConnectivityNode

__all__ = ["Terminal"]


@dataslot
class Terminal(AcDcTerminal):
    """
    An AC electrical connection point to a piece of conducting equipment. Terminals are connected at physical connection points called connectivity nodes.
    """

    conducting_equipment: ConductingEquipment | None = NoResetDescriptor(None)
    """The conducting equipment of the terminal. Conducting equipment have terminals that may be connected to other conducting equipment terminals via
    connectivity nodes."""

    phases: PhaseCode = PhaseCode.ABC
    """Represents the normal network phasing condition. If the attribute is missing three phases (ABC) shall be assumed."""

    traced_phases: TracedPhases = instantiate(TracedPhases)
    """the phase object representing the traced phases in both the normal and current network. If properly configured you would expect the normal state phases 
    to match those in `phases`"""

    sequence_number: int = 0
    """The orientation of the terminal connections for a multiple terminal conducting equipment. The sequence numbering starts with 1 and additional
    terminals should follow in increasing order. The first terminal is the "starting point" for a two terminal branch."""

    normal_feeder_direction: FeederDirection = FeederDirection.NONE
    """ Stores the direction of the feeder head relative to this [Terminal] in the normal state of the network.
    """

    current_feeder_direction: FeederDirection = FeederDirection.NONE
    """ Stores the direction of the feeder head relative to this [Terminal] in the current state of the network.
    """

    connectivity_node: ConnectivityNode | None = WeakrefDescriptor()
    """This is a weak reference to the connectivity node so if a Network object goes out of scope, holding a single conducting equipment
    reference does not cause everything connected to it in the network to stay in memory."""

    @property
    def normal_phases(self) -> PhaseStatus:
        """ Convenience method for accessing the normal phases"""
        return NormalPhases(self)

    @property
    def current_phases(self) -> PhaseStatus:
        """ Convenience method for accessing the current phases"""
        return CurrentPhases(self)

    @property
    def connected(self) -> bool:
        if self.connectivity_node:
            return True
        return False

    @property
    def connectivity_node_id(self):
        return self.connectivity_node.mrid if self.connectivity_node is not None else None

    def __repr__(self):
        return f"Terminal{{{self.mrid}}}"

    def get_switch(self):
        """
        Get any associated switch for this Terminal
        Returns Switch if present in this terminals ConnectivityNode, else None
        """
        return self.connectivity_node.get_switch()

    @property
    def base_voltage(self):
        return self.conducting_equipment.get_base_voltage(self)

    def connected_terminals(self) -> Generator[Terminal]:
        """
        Get the terminals that are connected to this `Terminal`.

        :return: A `Generator` of terminals that are connected to this `Terminal`.
        """
        for t in self.connectivity_node.terminals if self.connectivity_node else []:
            if t is not self:
                yield t

    def other_terminals(self) -> Generator[Terminal]:
        """
        * Get the terminals that share the same `ConductingEquipment` as this `Terminal`.
        *
        :return: A `Generator` of terminals that share the same `ConductingEquipment` as this `Terminal`.
        """
        for t in self.conducting_equipment.terminals:
            if t is not self:
                yield t

    def connect(self, connectivity_node: ConnectivityNode):
        self.connectivity_node = connectivity_node

    def disconnect(self):
        self.connectivity_node = None

    def is_feeder_head_terminal(self):
        if self.conducting_equipment is None:
            return False

        for feeder in filter(lambda c: isinstance(c, Feeder), self.conducting_equipment.containers):
            if feeder.normal_head_terminal == self:
                return True

    def has_connected_busbars(self):
        try:
            return any(it != self and isinstance(it.conducting_equipment, BusbarSection) for it in self.connectivity_node.terminals) == True
        except AttributeError:
            return False
