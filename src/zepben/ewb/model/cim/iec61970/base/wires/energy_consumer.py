#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["EnergyConsumer"]

from typing import Optional, Generator, List, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61970.base.wires.energy_connection import EnergyConnection
from zepben.ewb.model.cim.iec61970.base.wires.phase_shunt_connection_kind import PhaseShuntConnectionKind
from zepben.ewb.util import nlen, get_by_mrid, ngen, safe_remove

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.energy_consumer_phase import EnergyConsumerPhase


@dataslot
@boilermaker
class EnergyConsumer(EnergyConnection):
    """Generic user of energy - a point of consumption on the power system phases. May also represent a pro-sumer with negative p/q values. """

    energy_consumer_phases: List[EnergyConsumerPhase] | None = MRIDListAccessor()
    """The individual phase models for this energy consumer."""

    customer_count: int | None = None
    """Number of individual customers represented by this demand."""

    grounded: bool | None = None
    """Used for Yn and Zn connections. True if the neutral is solidly grounded."""

    phase_connection: PhaseShuntConnectionKind = PhaseShuntConnectionKind.D
    """`zepben.protobuf.cim.iec61970.base.wires.phase_shunt_connection_kind.PhaseShuntConnectionKind` - The type of phase connection, 
    such as wye, delta, I (single phase)."""

    p: float | None = None
    """Active power of the load. Load sign convention is used, i.e. positive sign means flow out from a node. For voltage dependent loads the value is at 
    rated voltage. Starting value for a steady state solution."""

    p_fixed: float | None = None
    """Active power of the load that is a fixed quantity. Load sign convention is used, i.e. positive sign means flow out from a node."""

    q: float | None = None
    """Reactive power of the load. Load sign convention is used, i.e. positive sign means flow out from a node. For voltage dependent loads the value is at 
    rated voltage. Starting value for a steady state solution."""

    q_fixed: float | None = None
    """Power of the load that is a fixed quantity. Load sign convention is used, i.e. positive sign means flow out from a node."""

    def _retype(self):
        self.energy_consumer_phases: MRIDListRouter = ...
    
    @deprecated("BOILERPLATE: Use len(energy_consumer_phases) instead")
    def num_phases(self):
        return len(self.energy_consumer_phases)

    @property
    def phases(self) -> Generator[EnergyConsumerPhase, None, None]:
        """The individual phase models for this energy consumer."""
        return ngen(self.energy_consumer_phases)

    @deprecated("BOILERPLATE: Use energy_consumer_phases.get_by_mrid(mrid) instead")
    def get_phase(self, mrid: str) -> EnergyConsumerPhase:
        return self.energy_consumer_phases.get_by_mrid(mrid)

    @deprecated("BOILERPLATE: Use energy_consumer_phases.append(phase) instead")
    def add_phase(self, phase: EnergyConsumerPhase) -> EnergyConsumer:
        return self.energy_consumer_phases.append(phase)

    @deprecated("BOILERPLATE: Use energy_consumer_phases.remove(phase) instead")
    def remove_phase(self, phase: EnergyConsumerPhase) -> EnergyConsumer:
        return self.energy_consumer_phases.remove(phase)

    @deprecated("BOILERPLATE: Use energy_consumer_phases.clear() instead")
    def clear_phases(self) -> EnergyConsumer:
        return self.energy_consumer_phases.clear()
        return self
