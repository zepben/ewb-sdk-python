#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["EnergySourcePhase"]

from typing import Optional, TYPE_CHECKING

from zepben.ewb.dataslot import dataslot, NoResetDescriptor
from zepben.ewb.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.ewb.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.energy_source import EnergySource


@dataslot
class EnergySourcePhase(PowerSystemResource):
    """
    A single phase of an energy source.
    """

    energy_source: Optional['EnergySource'] = NoResetDescriptor(None)
    """The `zepben.ewb.model.cim.iec61970.wires.EnergySource` with this `EnergySourcePhase`"""

    phase: SinglePhaseKind = SinglePhaseKind.NONE
    """A `zepben.ewb.model.cim.iec61970.base.wires.single_phase_kind.SinglePhaseKind` Phase of this energy source component. If the energy source is wye connected, 
    the connection is from the indicated phase to the central ground or neutral point. If the energy source is delta connected, the phase indicates an energy 
    source connected from the indicated phase to the next logical non-neutral phase."""
