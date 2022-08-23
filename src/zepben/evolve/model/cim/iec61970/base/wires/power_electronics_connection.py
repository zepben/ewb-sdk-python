#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import Optional, List, Generator, TYPE_CHECKING

if TYPE_CHECKING:
    from zepben.evolve import PowerElectronicsUnit

from zepben.evolve.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.evolve.model.cim.iec61970.base.wires.energy_connection import RegulatingCondEq
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.evolve.util import ngen, nlen, get_by_mrid, safe_remove

__all__ = ["PowerElectronicsConnection", "PowerElectronicsConnectionPhase"]


class PowerElectronicsConnectionPhase(PowerSystemResource):
    """A single phase of a power electronics connection."""

    power_electronics_connection: Optional[PowerElectronicsConnection] = None
    """The power electronics connection to which the phase belongs."""

    p: Optional[float] = None
    """Active power injection. Load sign convention is used, i.e. positive sign means flow into the equipment from the network."""

    phase: SinglePhaseKind = SinglePhaseKind.X
    """
    Phase of this energy producer component. If the energy producer is wye connected, the connection is from the indicated phase to the central
    ground or neutral point. If the energy producer is delta connected, the phase indicates an energy producer connected from the indicated phase to the next
    logical non-neutral phase.
    """

    q: Optional[float] = None
    """Reactive power injection. Load sign convention is used, i.e. positive sign means flow into the equipment from the network."""


class PowerElectronicsConnection(RegulatingCondEq):
    """
    A connection to the AC network for energy production or consumption that uses power electronics rather than rotating machines.
    """

    max_i_fault: Optional[int] = None
    """Maximum fault current this device will contribute, in per-unit of rated current, before the converter protection will trip or bypass."""

    p: Optional[float] = None
    """Active power injection. Load sign convention is used, i.e. positive sign means flow out from a node. Starting value for a steady state solution."""

    q: Optional[float] = None
    """Reactive power injection. Load sign convention is used, i.e. positive sign means flow out from a node. Starting value for a steady state solution."""

    max_q: Optional[float] = None
    """Maximum reactive power limit. This is the maximum (nameplate) limit for the unit."""

    min_q: Optional[float] = None
    """Minimum reactive power limit for the unit. This is the minimum (nameplate) limit for the unit."""

    rated_s: Optional[int] = None
    """Nameplate apparent power rating for the unit. The attribute shall have a positive value."""

    rated_u: Optional[int] = None
    """Rated voltage (nameplate data, Ur in IEC 60909-0). It is primarily used for short circuit data exchange according to IEC 60909. 
    The attribute shall be a positive value."""

    _power_electronics_units: Optional[List[PowerElectronicsUnit]] = None
    """An AC network connection may have several power electronics units connecting through it."""

    _power_electronics_connection_phases: Optional[List[PowerElectronicsConnectionPhase]] = None
    """The individual units models for the power electronics connection."""

    def __init__(self, power_electronics_units: List[PowerElectronicsUnit] = None,
                 power_electronics_connection_phases: List[PowerElectronicsConnectionPhase] = None, **kwargs):
        super(PowerElectronicsConnection, self).__init__(**kwargs)
        if power_electronics_units:
            for unit in power_electronics_units:
                self.add_unit(unit)

        if power_electronics_connection_phases:
            for phase in power_electronics_connection_phases:
                self.add_phase(phase)

    @property
    def units(self) -> Generator[PowerElectronicsUnit, None, None]:
        """
        The `PowerElectronicsUnit`s for this `PowerElectronicsConnection`.
        """
        return ngen(self._power_electronics_units)

    @property
    def phases(self) -> Generator[PowerElectronicsConnectionPhase, None, None]:
        """
        The `PowerElectronicsConnectionPhase`s for this `PowerElectronicsConnection`.
        """
        return ngen(self._power_electronics_connection_phases)

    def has_units(self):
        """
        Check if this connection has any associated `PowerElectronicsUnit`s
        Returns True if there is at least one `PowerElectronicsUnit`, otherwise False
        """
        return nlen(self._power_electronics_units) > 0

    def num_units(self):
        """Return the number of `PowerElectronicsUnit`s associated with this `PowerElectronicsConnection`"""
        return nlen(self._power_electronics_units)

    def get_unit(self, mrid: str) -> PowerElectronicsUnit:
        """
        Get the `PowerElectronicsUnit` for this
        `PowerElectronicsConnection` identified by `mrid`

        `mrid` the mRID of the required `PowerElectronicsUnit`
        Returns The `PowerElectronicsUnit` with the specified `mrid`
        if it exists

        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._power_electronics_units, mrid)

    def add_unit(self, unit: PowerElectronicsUnit) -> PowerElectronicsConnection:
        """
        Associate an `PowerElectronicsUnit` with this
        `PowerElectronicsConnection`

        `unit` the `PowerElectronicsUnit` to associate with this `PowerElectronicsConnection`.
        Returns A reference to this `PowerElectronicsConnection` to allow fluent use.
        Raises `ValueError` if another `PowerElectronicsUnit` with the same `mrid` already exists for this `PowerElectronicsConnection`.
        """
        if self._validate_reference(unit, self.get_unit, "A PowerElectronicsUnit"):
            return self
        self._power_electronics_units = list() if self._power_electronics_units is None else self._power_electronics_units
        self._power_electronics_units.append(unit)
        return self

    def remove_unit(self, unit: PowerElectronicsUnit) -> PowerElectronicsConnection:
        """
        Disassociate `unit` from this `PowerElectronicsConnection`

        `unit` the `PowerElectronicsUnit` to disassociate from this `PowerElectronicsConnection`.
        Returns A reference to this `PowerElectronicsConnection` to allow fluent use.
        Raises `ValueError` if `unit` was not associated with this `PowerElectronicsConnection`.
        """
        self._power_electronics_units = safe_remove(self._power_electronics_units, unit)
        return self

    def clear_units(self) -> PowerElectronicsConnection:
        """
        Clear all units.
        Returns A reference to this `PowerElectronicsConnection` to allow fluent use.
        """
        self._power_electronics_units = None
        return self

    def has_phases(self):
        """
        Check if this connection has any associated `PowerElectronicsConnectionPhase`s
        Returns True if there is at least one `PowerElectronicsConnectionPhase`, otherwise False
        """
        return nlen(self._power_electronics_connection_phases) > 0

    def num_phases(self):
        """Return the number of `PowerElectronicsConnectionPhase`s associated with this `PowerElectronicsConnection`"""
        return nlen(self._power_electronics_connection_phases)

    def get_phase(self, mrid: str) -> PowerElectronicsConnectionPhase:
        """
        Get the `PowerElectronicsConnectionPhase` for this `PowerElectronicsConnection` identified by `mrid`

        `mrid` the mRID of the required `PowerElectronicsConnectionPhase`
        Returns The `PowerElectronicsConnectionPhase` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._power_electronics_connection_phases, mrid)

    def add_phase(self, phase: PowerElectronicsConnectionPhase) -> PowerElectronicsConnection:
        """
        Associate a `PowerElectronicsConnectionPhase` with this `PowerElectronicsConnection`

        `phase` the `PowerElectronicsConnectionPhase` to associate with this `PowerElectronicsConnection`.
        Returns A reference to this `PowerElectronicsConnection` to allow fluent use.
        Raises `ValueError` if another `PowerElectronicsConnectionPhase` with the same `mrid` already exists for this `PowerElectronicsConnection`.
        """
        if self._validate_reference(phase, self.get_phase, "A PowerElectronicsConnectionPhase"):
            return self
        self._power_electronics_connection_phases = list() if self._power_electronics_connection_phases is None else self._power_electronics_connection_phases
        self._power_electronics_connection_phases.append(phase)
        return self

    def remove_phase(self, phase: PowerElectronicsConnectionPhase) -> PowerElectronicsConnection:
        """
        Disassociate `phase` from this `PowerElectronicsConnection`

        `phase` the `PowerElectronicsConnectionPhase` to disassociate from this `PowerElectronicsConnection`.
        Returns A reference to this `PowerElectronicsConnection` to allow fluent use.
        Raises `ValueError` if `phase` was not associated with this `PowerElectronicsConnection`.
        """
        self._power_electronics_connection_phases = safe_remove(self._power_electronics_connection_phases, phase)
        return self

    def clear_phases(self) -> PowerElectronicsConnection:
        """
        Clear all phases.
        Returns A reference to this `PowerElectronicsConnection` to allow fluent use.
       """
        self._power_electronics_connection_phases = None
        return self
