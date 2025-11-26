#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["EnergyConsumerPhase"]

from typing import Optional, TYPE_CHECKING

from zepben.ewb.dataslot import dataslot, NoResetDescriptor
from zepben.ewb.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.ewb.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.energy_consumer import EnergyConsumer


@dataslot
class EnergyConsumerPhase(PowerSystemResource):
    """A single phase of an energy consumer."""

    energy_consumer: Optional['EnergyConsumer'] = NoResetDescriptor(None)

    phase: SinglePhaseKind = SinglePhaseKind.X
    """Phase of this energy consumer component. If the energy consumer is wye connected, the connection is from the indicated phase to the central ground or 
    neutral point. If the energy consumer is delta connected, the phase indicates an energy consumer connected from the indicated phase to the next
    logical non-neutral phase. """

    p: float | None = None
    """Active power of the load. Load sign convention is used, i.e. positive sign means flow out from a node. For voltage dependent loads the value is at 
    rated voltage. Starting value for a steady state solution."""

    q: float | None = None
    """Reactive power of the load. Load sign convention is used, i.e. positive sign means flow out from a node. For voltage dependent loads the value is at 
    rated voltage. Starting value for a steady state solution."""

    p_fixed: float | None = None
    """Active power of the load that is a fixed quantity. Load sign convention is used, i.e. positive sign means flow out from a node."""

    q_fixed: float | None = None
    """Reactive power of the load that is a fixed quantity. Load sign convention is used, i.e. positive sign means flow out from a node."""

