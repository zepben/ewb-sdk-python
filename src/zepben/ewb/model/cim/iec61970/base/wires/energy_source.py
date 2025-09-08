#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["EnergySource"]

from typing import List, Optional, TYPE_CHECKING

from zepben.ewb.collections.autoslot import dataslot
from zepben.ewb.collections.mrid_list import MRIDList
from zepben.ewb.model.cim.iec61970.base.wires.energy_connection import EnergyConnection

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.energy_source_phase import EnergySourcePhase


@dataslot
class EnergySource(EnergyConnection):
    """
    A generic equivalent for an energy supplier on a transmission or distribution voltage level.
    """

    energy_source_phases: Optional[List[EnergySourcePhase]] = None

    active_power: Optional[float] = None
    """
    High voltage source active injection. Load sign convention is used, i.e. positive sign means flow out from a node. Starting value
    for steady state solutions
    """

    reactive_power: Optional[float] = None
    """High voltage source reactive injection. Load sign convention is used, i.e. positive sign means flow out from a node. 
    Starting value for steady state solutions."""

    voltage_angle: Optional[float] = None
    """Phase angle of a-phase open circuit."""

    voltage_magnitude: Optional[float] = None
    """Phase-to-phase open circuit voltage magnitude."""

    p_max: Optional[float] = None
    """
    This is the maximum active power that can be produced by the source. Load sign convention is used, i.e. positive sign means flow out from a
    TopologicalNode (bus) into the conducting equipment.
    """

    p_min: Optional[float] = None
    """
    This is the minimum active power that can be produced by the source. Load sign convention is used, i.e. positive sign means flow out from a
    TopologicalNode (bus) into the conducting equipment.
    """

    r: Optional[float] = None
    """Positive sequence Thevenin resistance."""

    r0: Optional[float] = None
    """Zero sequence Thevenin resistance."""

    rn: Optional[float] = None
    """Negative sequence Thevenin resistance."""

    x: Optional[float] = None
    """Positive sequence Thevenin reactance."""

    x0: Optional[float] = None
    """Zero sequence Thevenin reactance."""

    xn: Optional[float] = None
    """Negative sequence Thevenin reactance."""

    is_external_grid: bool = False
    """
    True if this energy source represents the higher-level power grid connection to an external grid
    that normally is modelled as the slack bus for power flow calculations.
    """

    r_min: Optional[float] = None
    """Minimum positive sequence Thevenin resistance."""

    rn_min: Optional[float] = None
    """Minimum negative sequence Thevenin resistance."""

    r0_min: Optional[float] = None
    """Minimum zero sequence Thevenin resistance."""

    x_min: Optional[float] = None
    """Minimum positive sequence Thevenin reactance."""

    xn_min: Optional[float] = None
    """Minimum negative sequence Thevenin reactance."""

    x0_min: Optional[float] = None
    """Minimum zero sequence Thevenin reactance."""

    r_max: Optional[float] = None
    """Maximum positive sequence Thevenin resistance."""

    rn_max: Optional[float] = None
    """Maximum negative sequence Thevenin resistance."""

    r0_max: Optional[float] = None
    """Maximum zero sequence Thevenin resistance."""

    x_max: Optional[float] = None
    """Maximum positive sequence Thevenin reactance."""

    xn_max: Optional[float] = None
    """Maximum negative sequence Thevenin reactance."""

    x0_max: Optional[float] = None
    """Maximum zero sequence Thevenin reactance."""

    def __post_init__(self):
        self.energy_source_phases: MRIDList[EnergySourcePhase] = MRIDList(self.energy_source_phases)

    @property
    def phases(self):
        """
        The `EnergySourcePhase`s for this `EnergySource`.
        """
        return self.energy_source_phases

    def num_phases(self):
        """Return the number of `EnergySourcePhase`s associated with this `EnergySource`"""
        return len(self.energy_source_phases)

    def get_phase(self, mrid: str) -> EnergySourcePhase:
        """
        Get the `EnergySourcePhase` for this `EnergySource` identified by `mrid`

        `mrid` the mRID of the required `EnergySourcePhase`
        Returns The `EnergySourcePhase` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return self.energy_source_phases.get_by_mrid(mrid)

    def add_phase(self, phase: EnergySourcePhase) -> EnergySource:
        """
        Associate an `EnergySourcePhase` with this `EnergySource`

        `phase` the `EnergySourcePhase` to associate with this `EnergySource`.
        Returns A reference to this `EnergySource` to allow fluent use.
        Raises `ValueError` if another `EnergySourcePhase` with the same `mrid` already exists for this `EnergySource`.
        """
        self.energy_source_phases.add(phase)
        return self

    def remove_phase(self, phase: EnergySourcePhase) -> EnergySource:
        """
        Disassociate an `phase` from this `EnergySource`

        `phase` the `EnergySourcePhase` to disassociate from this `EnergySource`.
        Returns A reference to this `EnergySource` to allow fluent use.
        Raises `ValueError` if `phase` was not associated with this `EnergySource`.
        """
        self.energy_source_phases.remove(phase)
        return self

    def clear_phases(self) -> EnergySource:
        """
        Clear all phases.
        Returns A reference to this `EnergySource` to allow fluent use.
        """
        self.energy_source_phases.clear()
        return self
