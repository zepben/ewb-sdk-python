#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["PowerElectronicsConnectionPhase"]

from typing import Optional, TYPE_CHECKING

from typing_extensions import deprecated

from zepben.ewb.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.ewb.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.ewb.dataclass_descriptors.dataclass_base import zb_dataclass

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.power_electronics_connection import PowerElectronicsConnection


@zb_dataclass
class PowerElectronicsConnectionPhase(PowerSystemResource):
    """A single phase of a power electronics connection."""

    _power_electronics_connection: Optional['PowerElectronicsConnection'] = None

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

    @property
    def power_electronics_connection(self):
        """The power electronics connection to which the phase belongs."""
        return self._power_electronics_connection

    @power_electronics_connection.setter
    @deprecated("power_electronics_connection should never be set directly - it is automatically set when adding it to the `phases` list")
    def power_electronics_connection(self, value):
        self._power_electronics_connection = value