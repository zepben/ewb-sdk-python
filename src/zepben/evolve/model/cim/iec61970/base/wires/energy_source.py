#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import List, Optional
from collections.abc import Generator

from zepben.evolve.model.cim.iec61970.base.wires.energy_connection import EnergyConnection
from zepben.evolve.model.cim.iec61970.base.wires.energy_source_phase import EnergySourcePhase
from zepben.evolve.util import nlen, get_by_mrid, ngen, safe_remove

__all__ = ["EnergySource"]


class EnergySource(EnergyConnection):
    """
    A generic equivalent for an energy supplier on a transmission or distribution voltage level.
    """

    _energy_source_phases: List[EnergySourcePhase] | None = None

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

    is_external_grid: bool = False
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

    def __init__(self, energy_source_phases: List[EnergySourcePhase] = None, **kwargs):
        super(EnergySource, self).__init__(**kwargs)
        if energy_source_phases:
            for phase in energy_source_phases:
                self.add_phase(phase)

    @property
    def phases(self) -> Generator[EnergySourcePhase, None, None]:
        """
        The `EnergySourcePhase`s for this `EnergySource`.
        """
        return ngen(self._energy_source_phases)

    def num_phases(self):
        """Return the number of `EnergySourcePhase`s associated with this `EnergySource`"""
        return nlen(self._energy_source_phases)

    def get_phase(self, mrid: str) -> EnergySourcePhase:
        """
        Get the `EnergySourcePhase` for this `EnergySource` identified by `mrid`

        `mrid` the mRID of the required `EnergySourcePhase`
        Returns The `EnergySourcePhase` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._energy_source_phases, mrid)

    def add_phase(self, phase: EnergySourcePhase) -> EnergySource:
        """
        Associate an `EnergySourcePhase` with this `EnergySource`

        `phase` the `EnergySourcePhase` to associate with this `EnergySource`.
        Returns A reference to this `EnergySource` to allow fluent use.
        Raises `ValueError` if another `EnergySourcePhase` with the same `mrid` already exists for this `EnergySource`.
        """
        if self._validate_reference(phase, self.get_phase, "An EnergySourcePhase"):
            return self
        self._energy_source_phases = list() if self._energy_source_phases is None else self._energy_source_phases
        self._energy_source_phases.append(phase)
        return self

    def remove_phase(self, phase: EnergySourcePhase) -> EnergySource:
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
