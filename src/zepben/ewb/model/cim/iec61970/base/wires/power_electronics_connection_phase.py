#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["PowerElectronicsConnectionPhase"]

from typing import Optional, TYPE_CHECKING

from zepben.ewb.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.ewb.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.power_electronics_connection import PowerElectronicsConnection


class PowerElectronicsConnectionPhase(PowerSystemResource):
    """A single phase of a power electronics connection."""

    power_electronics_connection: Optional['PowerElectronicsConnection'] = None
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
