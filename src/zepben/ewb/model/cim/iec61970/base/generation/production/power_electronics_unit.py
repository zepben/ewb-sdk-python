#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["PowerElectronicsUnit"]

from typing import Optional, TYPE_CHECKING

from zepben.ewb.model.cim.iec61970.base.core.equipment import Equipment

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.power_electronics_connection import PowerElectronicsConnection


class PowerElectronicsUnit(Equipment):
    """
    A generating unit or battery or aggregation that connects to the AC network using power electronics rather than rotating machines.
    """

    power_electronics_connection: Optional['PowerElectronicsConnection'] = None
    """An AC network connection may have several power electronics units connecting through it."""

    max_p: Optional[int] = None
    """Maximum active power limit. This is the maximum (nameplate) limit for the unit."""

    min_p: Optional[int] = None
    """Minimum active power limit. This is the minimum (nameplate) limit for the unit."""
