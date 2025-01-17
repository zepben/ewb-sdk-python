#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from zepben.evolve.model.cim.extensions.iec61970.base.wires.battery_control_mode import BatteryControlMode
from zepben.evolve.model.cim.extensions.zbex import zbex
from zepben.evolve.model.cim.iec61970.base.wires.regulating_control import RegulatingControl

if TYPE_CHECKING:
    pass

__all__ = ["BatteryControl", "BatteryControlMode"]


@zbex
class BatteryControl(RegulatingControl):
    """
    [ZBEX] Describes behaviour specific to controlling batteries.
    """

    charging_rate: Optional[float] = None
    """[ZBEX] Charging rate (input power) in percentage of maxP. (Unit: PerCent)"""

    discharging_rate: Optional[float] = None
    """[ZBEX] Discharge rate (output power) in percentage of maxP. (Unit: PerCent)"""

    reserve_percent: Optional[float] = None
    """
    [ZBEX] 
    Percentage of the rated storage capacity that should be reserved during normal operations. This reserve acts as a safeguard, preventing the energy level 
    from dropping below this threshold under standard conditions. The field must be set to a non-negative value between 0 and 1. (Unit: PerCent)
    """

    control_mode: BatteryControlMode = BatteryControlMode.UNKNOWN
    """[ZBEX] Mode of operation for the dispatch (charging/discharging) function of BatteryControl."""
