#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["EnergySource"]

from typing import List, Optional, Generator, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61970.base.wires.energy_connection import EnergyConnection
from zepben.ewb.util import nlen, get_by_mrid, ngen, safe_remove

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.energy_source_phase import EnergySourcePhase


@dataslot
@boilermaker
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
        self.energy_source_phases: MRIDListRouter = ...
    
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

    @deprecated("BOILERPLATE: Use energy_source_phases.append(phase) instead")
    def add_phase(self, phase: EnergySourcePhase) -> EnergySource:
        return self.energy_source_phases.append(phase)

    @deprecated("BOILERPLATE: Use energy_source_phases.remove(phase) instead")
    def remove_phase(self, phase: EnergySourcePhase) -> EnergySource:
        return self.energy_source_phases.remove(phase)

    @deprecated("BOILERPLATE: Use energy_source_phases.clear() instead")
    def clear_phases(self) -> EnergySource:
        self.energy_source_phases.clear()
        return self

