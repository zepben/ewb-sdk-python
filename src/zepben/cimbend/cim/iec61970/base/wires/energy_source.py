#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import List, Optional, Generator

from zepben.cimbend.cim.iec61970.base.wires.energy_connection import EnergyConnection
from zepben.cimbend.cim.iec61970.base.wires.energy_source_phase import EnergySourcePhase
from zepben.cimbend.util import nlen, get_by_mrid, ngen, safe_remove

__all__ = ["EnergySource"]


class EnergySource(EnergyConnection):
    """
    A generic equivalent for an energy supplier on a transmission or distribution voltage level.
    """

    _energy_source_phases: Optional[List[EnergySourcePhase]] = None
    active_power: float = 0.0
    """High voltage source active injection. Load sign convention is used, i.e. positive sign means flow out from a node. Starting value for steady state solutions"""

    r: float = 0.0
    """Positive sequence Thevenin resistance."""

    x: float = 0.0
    """Positive sequence Thevenin reactance."""

    reactive_power: float = 0.0
    """High voltage source reactive injection. Load sign convention is used, i.e. positive sign means flow out from a node. 
    Starting value for steady state solutions."""

    voltage_angle: float = 0.0
    """Phase angle of a-phase open circuit."""

    voltage_magnitude: float = 0.0
    """Phase-to-phase open circuit voltage magnitude."""

    p_max: float = 0.0
    p_min: float = 0.0
    r0: float = 0.0
    rn: float = 0.0
    x0: float = 0.0
    xn: float = 0.0

    def __init__(self, usage_points: List[UsagePoint] = None, equipment_containers: List[EquipmentContainer] = None,
                 operational_restrictions: List[OperationalRestriction] = None, current_feeders: List[Feeder] = None, terminals: List[Terminal] = None,
                 energy_source_phases: List[EnergySourcePhase] = None):
        super(EnergySource, self).__init__(usage_points=usage_points, equipment_containers=equipment_containers,
                                           operational_restrictions=operational_restrictions,
                                           current_feeders=current_feeders, terminals=terminals)
        if energy_source_phases:
            for phase in energy_source_phases:
                self.add_phase(phase)

    @property
    def phases(self) -> Generator[EnergySourcePhase, None, None]:
        """
        The `EnergySourcePhase`s for this `EnergySource`.
        """
        return ngen(self._energy_source_phases)

    def has_phases(self):
        """
        Check if this source has any associated `EnergySourcePhase`s
        Returns True if there is at least one `EnergySourcePhase`, otherwise False
        """
        return nlen(self._energy_source_phases) > 0

    def num_phases(self):
        """Return the number of `EnergySourcePhase`s associated with this `EnergySource`"""
        return nlen(self._energy_source_phases)

    def get_phase(self, mrid: str) -> EnergySource:
        """
        Get the `zepben.cimbend.cim.iec61970.base.wires.energy_source_phase.EnergySourcePhase` for this `EnergySource` identified by `mrid`

        `mrid` the mRID of the required `zepben.cimbend.cim.iec61970.base.wires.energy_source_phase.EnergySourcePhase`
        Returns The `zepben.cimbend.cim.iec61970.base.wires.energy_source_phase.EnergySourcePhase` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._energy_source_phases, mrid)

    def add_phase(self, phase: EnergySourcePhase) -> EnergySource:
        """
        Associate an `zepben.cimbend.cim.iec61970.base.wires.energy_source_phase.EnergySourcePhase` with this `EnergySource`

        `phase` the `EnergySourcePhase` to associate with this `EnergySource`.
        Returns A reference to this `EnergySource` to allow fluent use.
        Raises `ValueError` if another `EnergySourcePhase` with the same `mrid` already exists for this `EnergySource`.
        """
        if self._validate_reference(phase, self.get_phase, "An EnergySourcePhase"):
            return self
        self._energy_source_phases = list() if self._energy_source_phases is None else self._energy_source_phases
        self._energy_source_phases.append(phase)
        return self

    def remove_phases(self, phase: EnergySourcePhase) -> EnergySource:
        """
        Disassociate an `phase` from this `EnergySource`

        `phase` the `EnergySourcePhase` to disassociate from this `EnergySource`.
        Returns A reference to this `EnergySource` to allow fluent use.
        Raises `ValueError` if `phase` was not associated with this `EnergySource`.
        """
        self._energy_source_phases = safe_remove(self._energy_source_phases, phase)
        return self

    def clear_phases(self) -> EnergySource:
        """
        Clear all phases.
        Returns A reference to this `EnergySource` to allow fluent use.
        """
        self._energy_source_phases = None
        return self
