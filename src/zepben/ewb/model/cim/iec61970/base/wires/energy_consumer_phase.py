#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["EnergyConsumerPhase"]

from typing import Optional, TYPE_CHECKING

from zepben.ewb.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.ewb.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.energy_consumer import EnergyConsumer


class EnergyConsumerPhase(PowerSystemResource):
    """A single phase of an energy consumer."""

    _energy_consumer: Optional['EnergyConsumer'] = None

    phase: SinglePhaseKind = SinglePhaseKind.X
    """Phase of this energy consumer component. If the energy consumer is wye connected, the connection is from the indicated phase to the central ground or 
    neutral point. If the energy consumer is delta connected, the phase indicates an energy consumer connected from the indicated phase to the next
    logical non-neutral phase. """

    p: Optional[float] = None
    """Active power of the load. Load sign convention is used, i.e. positive sign means flow out from a node. For voltage dependent loads the value is at 
    rated voltage. Starting value for a steady state solution."""

    q: Optional[float] = None
    """Reactive power of the load. Load sign convention is used, i.e. positive sign means flow out from a node. For voltage dependent loads the value is at 
    rated voltage. Starting value for a steady state solution."""

    p_fixed: Optional[float] = None
    """Active power of the load that is a fixed quantity. Load sign convention is used, i.e. positive sign means flow out from a node."""

    q_fixed: Optional[float] = None
    """Reactive power of the load that is a fixed quantity. Load sign convention is used, i.e. positive sign means flow out from a node."""

    def __init__(self, energy_consumer: 'EnergyConsumer' = None, **kwargs):
        super(EnergyConsumerPhase, self).__init__(**kwargs)
        if energy_consumer:
            self.energy_consumer = energy_consumer

    @property
    def energy_consumer(self):
        """The `EnergyConsumer` that has this phase."""
        return self._energy_consumer

    @energy_consumer.setter
    def energy_consumer(self, ec):
        if self._energy_consumer is None or self._energy_consumer is ec:
            self._energy_consumer = ec
        else:
            raise ValueError(f"energy_consumer for {str(self)} has already been set to {self._energy_consumer}, cannot reset this field to {ec}")
