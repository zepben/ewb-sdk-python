#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["EnergySource"]

from typing import List, Optional, Generator, TYPE_CHECKING
from dataclasses import field
from typing_extensions import deprecated

from zepben.ewb.model.cim.iec61970.base.wires.energy_connection import EnergyConnection
from zepben.ewb.util import nlen, get_by_mrid, ngen, safe_remove, require
from zepben.ewb.dataclass_descriptors.dataclass_base import zb_dataclass
from zepben.ewb import remove_descriptor_annotations, Alias
from zepben.ewb.dataclass_descriptors.mrid_list import MridCollection, LazyMridList

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.energy_source_phase import EnergySourcePhase


@zb_dataclass
class EnergySource(EnergyConnection):
    """
    A generic equivalent for an energy supplier on a transmission or distribution voltage level.
    """

    _energy_source_phases: Optional[List[EnergySourcePhase]] = field(default=None)

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

    is_external_grid: Optional[bool] = None
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

    phases: MridCollection[EnergySourcePhase] = LazyMridList(
        _energy_source_phases,
        "An EnergySourcePhase",
    )
    energy_source_phases = Alias(phases)


    # region deprecated list boilerplate
    # region phases boilerplate

    @deprecated("Use len(obj.phases) instead.")
    def num_phases(self):
        return len(self.phases)

    @deprecated("Use obj.phases.get_by_mrid(mrid) instead.")
    def get_phase(self, mrid: str) -> EnergySourcePhase:
        return self.phases.get_by_mrid(mrid)

    def add_phase(self, phase: EnergySourcePhase) -> EnergySource:
        """
        Associate an `EnergySourcePhase` with this `EnergySource`

        `phase` the `EnergySourcePhase` to associate with this `EnergySource`.
        Returns A reference to this `EnergySource` to allow fluent use.
        Raises `ValueError` if another `EnergySourcePhase` with the same `mrid` already exists for this `EnergySource`, or if `phase.energy_source` is not
        this `EnergySource`.
        """
        if self._validate_reference(phase, self.get_phase, "An EnergySourcePhase"):
            return self

        if phase.energy_source is None:
            phase.energy_source = self

        require(phase.energy_source is self, lambda: f"{phase} `energy_source` property references {phase.energy_source}, expected {self}.")

        self._energy_source_phases = list() if self._energy_source_phases is None else self._energy_source_phases
        self._energy_source_phases.append(phase)
        return self

    @deprecated("Use obj.phases.remove(phase) instead.")
    def remove_phase(self, phase: EnergySourcePhase) -> EnergySource:
        self.phases.remove(phase)
        return self

    @deprecated("Use obj.phases.clear() instead.")
    def clear_phases(self) -> EnergySource:
        self.phases.clear()
        return self

    # endregion phases boilerplate

    # endregion deprecated list boilerplate
