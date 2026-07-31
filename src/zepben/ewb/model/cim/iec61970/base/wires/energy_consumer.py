#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["EnergyConsumer"]

from dataclasses import field
from typing import Optional, List

from typing_extensions import deprecated

from zepben.ewb import Alias
from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb.boilerplate.collections.mrid_list import LazyMridList
from zepben.ewb.boilerplate.collections.mrid_collection import MridCollection
from zepben.ewb.boilerplate.backfill import Backfill
from zepben.ewb.model.cim.iec61970.base.wires.energy_connection import EnergyConnection
from zepben.ewb.model.cim.iec61970.base.wires.energy_consumer_phase import EnergyConsumerPhase
from zepben.ewb.model.cim.iec61970.base.wires.phase_shunt_connection_kind import PhaseShuntConnectionKind


@zb_dataclass
class EnergyConsumer(EnergyConnection):
    """Generic user of energy - a point of consumption on the power system phases. May also represent a pro-sumer with negative p/q values. """

    _energy_consumer_phases: Optional[List[EnergyConsumerPhase]] = field(default=None)
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

    def __init__(self, *args, energy_consumer_phases=None, **kwargs):
        super(EnergyConsumer, self).__init__(*args, **kwargs)
        self.phases.extend(energy_consumer_phases)

    phases: MridCollection[EnergyConsumerPhase] = LazyMridList(
        _energy_consumer_phases,
        "An EnergyConsumerPhase",
        backfill=Backfill(EnergyConsumerPhase.energy_consumer)
    )


    # region deprecated list boilerplate
    # region phases boilerplate

    @deprecated("Use len(obj.phases) instead.")
    def num_phases(self):
        return len(self.phases)

    @deprecated("Use obj.phases.get_by_mrid(mrid) instead.")
    def get_phase(self, mrid: str) -> EnergyConsumerPhase:
        return self.phases.get_by_mrid(mrid)

    @deprecated("Use obj.phases.append(phase) instead.")
    def add_phase(self, phase: EnergyConsumerPhase) -> EnergyConsumer:
        self.phases.append(phase)
        return self

    @deprecated("Use obj.phases.remove(phase) instead.")
    def remove_phase(self, phase: EnergyConsumerPhase) -> EnergyConsumer:
        self.phases.remove(phase)
        return self

    @deprecated("Use obj.phases.clear() instead.")
    def clear_phases(self) -> EnergyConsumer:
        self.phases.clear()
        return self

    # endregion phases boilerplate

    # endregion deprecated list boilerplate
