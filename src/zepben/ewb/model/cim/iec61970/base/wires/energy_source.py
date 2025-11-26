#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["EnergySource"]

from typing import List, Generator, TYPE_CHECKING

from typing_extensions import deprecated

from zepben.ewb.dataslot import MRIDListRouter, dataslot, MRIDListAccessor
from zepben.ewb.model.cim.iec61970.base.wires.energy_connection import EnergyConnection
from zepben.ewb.util import ngen

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.energy_source_phase import EnergySourcePhase


@dataslot
class EnergySource(EnergyConnection):
    """
    A generic equivalent for an energy supplier on a transmission or distribution voltage level.
    """

    energy_source_phases: List[EnergySourcePhase] | None = MRIDListAccessor()

    active_power: float | None = None
    """
    High voltage source active injection. Load sign convention is used, i.e. positive sign means flow out from a node. Starting value
    for steady state solutions
    """

    reactive_power: float | None = None
    """High voltage source reactive injection. Load sign convention is used, i.e. positive sign means flow out from a node. 
    Starting value for steady state solutions."""

    voltage_angle: float | None = None
    """Phase angle of a-phase open circuit."""

    voltage_magnitude: float | None = None
    """Phase-to-phase open circuit voltage magnitude."""

    p_max: float | None = None
    """
    This is the maximum active power that can be produced by the source. Load sign convention is used, i.e. positive sign means flow out from a
    TopologicalNode (bus) into the conducting equipment.
    """

    p_min: float | None = None
    """
    This is the minimum active power that can be produced by the source. Load sign convention is used, i.e. positive sign means flow out from a
    TopologicalNode (bus) into the conducting equipment.
    """

    r: float | None = None
    """Positive sequence Thevenin resistance."""

    r0: float | None = None
    """Zero sequence Thevenin resistance."""

    rn: float | None = None
    """Negative sequence Thevenin resistance."""

    x: float | None = None
    """Positive sequence Thevenin reactance."""

    x0: float | None = None
    """Zero sequence Thevenin reactance."""

    xn: float | None = None
    """Negative sequence Thevenin reactance."""

    is_external_grid: bool | None = None
    """
    True if this energy source represents the higher-level power grid connection to an external grid
    that normally is modelled as the slack bus for power flow calculations.
    """

    r_min: float | None = None
    """Minimum positive sequence Thevenin resistance."""

    rn_min: float | None = None
    """Minimum negative sequence Thevenin resistance."""

    r0_min: float | None = None
    """Minimum zero sequence Thevenin resistance."""

    x_min: float | None = None
    """Minimum positive sequence Thevenin reactance."""

    xn_min: float | None = None
    """Minimum negative sequence Thevenin reactance."""

    x0_min: float | None = None
    """Minimum zero sequence Thevenin reactance."""

    r_max: float | None = None
    """Maximum positive sequence Thevenin resistance."""

    rn_max: float | None = None
    """Maximum negative sequence Thevenin resistance."""

    r0_max: float | None = None
    """Maximum zero sequence Thevenin resistance."""

    x_max: float | None = None
    """Maximum positive sequence Thevenin reactance."""

    xn_max: float | None = None
    """Maximum negative sequence Thevenin reactance."""

    x0_max: float | None = None
    """Maximum zero sequence Thevenin reactance."""

    def _retype(self):
        self.energy_source_phases: MRIDListRouter[EnergySourcePhase] = ...
    
    @property
    def phases(self) -> Generator[EnergySourcePhase, None, None]:
        """
        The `EnergySourcePhase`s for this `EnergySource`.
        """
        return ngen(self.energy_source_phases)

    @deprecated("BOILERPLATE: Use len(energy_source_phases) instead")
    def num_phases(self):
        return len(self.energy_source_phases)

    @deprecated("BOILERPLATE: Use energy_source_phases.get_by_mrid(mrid) instead")
    def get_phase(self, mrid: str) -> EnergySourcePhase:
        return self.energy_source_phases.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use energy_source_phases.append(phase) instead")
    def add_phase(self, phase: EnergySourcePhase) -> EnergySource:
        self.energy_source_phases.append(phase)
        return self

    @deprecated("Boilerplate: Use energy_source_phases.remove(phase) instead")
    def remove_phase(self, phase: EnergySourcePhase) -> EnergySource:
        self.energy_source_phases.remove(phase)
        return self

    @deprecated("BOILERPLATE: Use energy_source_phases.clear() instead")
    def clear_phases(self) -> EnergySource:
        self.energy_source_phases.clear()
        return self

