#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["EnergyConsumer"]

from typing import Optional, Generator, List, TYPE_CHECKING

from zepben.ewb.model.cim.iec61970.base.wires.energy_connection import EnergyConnection
from zepben.ewb.model.cim.iec61970.base.wires.phase_shunt_connection_kind import PhaseShuntConnectionKind
from zepben.ewb.util import nlen, get_by_mrid, ngen, safe_remove

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.energy_consumer_phase import EnergyConsumerPhase


class EnergyConsumer(EnergyConnection):
    """Generic user of energy - a point of consumption on the power system phases. May also represent a pro-sumer with negative p/q values. """

    _energy_consumer_phases: Optional[List[EnergyConsumerPhase]] = None
    """The individual phase models for this energy consumer."""

    customer_count: Optional[int] = None
    """Number of individual customers represented by this demand."""

    grounded: Optional[bool] = None
    """Used for Yn and Zn connections. True if the neutral is solidly grounded."""

    phase_connection: PhaseShuntConnectionKind = PhaseShuntConnectionKind.D
    """`zepben.protobuf.cim.iec61970.base.wires.phase_shunt_connection_kind.PhaseShuntConnectionKind` - The type of phase connection, 
    such as wye, delta, I (single phase)."""

    p: Optional[float] = None
    """Active power of the load. Load sign convention is used, i.e. positive sign means flow out from a node. For voltage dependent loads the value is at 
    rated voltage. Starting value for a steady state solution."""

    p_fixed: Optional[float] = None
    """Active power of the load that is a fixed quantity. Load sign convention is used, i.e. positive sign means flow out from a node."""

    q: Optional[float] = None
    """Reactive power of the load. Load sign convention is used, i.e. positive sign means flow out from a node. For voltage dependent loads the value is at 
    rated voltage. Starting value for a steady state solution."""

    q_fixed: Optional[float] = None
    """Power of the load that is a fixed quantity. Load sign convention is used, i.e. positive sign means flow out from a node."""

    def __init__(self, energy_consumer_phases: List[EnergyConsumerPhase] = None, **kwargs):
        super(EnergyConsumer, self).__init__(**kwargs)
        if energy_consumer_phases:
            for phase in energy_consumer_phases:
                self.add_phase(phase)

    def num_phases(self):
        """Get the number of `EnergySourcePhase`s for this `EnergyConsumer`."""
        return nlen(self._energy_consumer_phases)

    @property
    def phases(self) -> Generator[EnergyConsumerPhase, None, None]:
        """The individual phase models for this energy consumer."""
        return ngen(self._energy_consumer_phases)

    def get_phase(self, mrid: str) -> EnergyConsumerPhase:
        """
        Get the `EnergyConsumerPhase` for this `EnergyConsumer` identified by `mrid`

        `mrid` The mRID of the required `EnergyConsumerPhase`
        Returns The `EnergyConsumerPhase` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._energy_consumer_phases, mrid)

    def add_phase(self, phase: EnergyConsumerPhase) -> EnergyConsumer:
        """
        Associate an `EnergyConsumerPhase` with this `EnergyConsumer`

        `phase` the `EnergyConsumerPhase` to associate with this `EnergyConsumer`.
        Returns A reference to this `EnergyConsumer` to allow fluent use.
        Raises `ValueError` if another `EnergyConsumerPhase` with the same `mrid` already exists for this `EnergyConsumer`.
        """
        if self._validate_reference(phase, self.get_phase, "An EnergyConsumerPhase"):
            return self
        self._energy_consumer_phases = list() if self._energy_consumer_phases is None else self._energy_consumer_phases
        self._energy_consumer_phases.append(phase)
        return self

    def remove_phase(self, phase: EnergyConsumerPhase) -> EnergyConsumer:
        """
        Disassociate `phase` from this `OperationalRestriction`.

        `phase` the `EnergyConsumerPhase` to disassociate with this `EnergyConsumer`.
        Raises `KeyError` if `phase` was not associated with this `EnergyConsumer`.
        Returns A reference to this `EnergyConsumer` to allow fluent use.
        Raises `ValueError` if `phase` was not associated with this `EnergyConsumer`.
        """
        self._energy_consumer_phases = safe_remove(self._energy_consumer_phases, phase)
        return self

    def clear_phases(self) -> EnergyConsumer:
        """
        Clear all phases.
        Returns A reference to this `EnergyConsumer` to allow fluent use.
        """
        self._energy_consumer_phases = None
        return self
