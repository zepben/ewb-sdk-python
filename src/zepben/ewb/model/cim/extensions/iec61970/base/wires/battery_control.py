#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["BatteryControl"]

from typing import Optional

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.extensions.iec61970.base.wires.battery_control_mode import BatteryControlMode
from zepben.ewb.model.cim.extensions.zbex import zbex
from zepben.ewb.model.cim.iec61970.base.wires.regulating_control import RegulatingControl


@zbex
@dataslot
class BatteryControl(RegulatingControl):
    """
    [ZBEX]
    Describes behaviour specific to controlling batteries.
    """

    charging_rate: float | None = None
    """[ZBEX] Charging rate (input power) in percentage of maxP. (Unit: PerCent)"""

    discharging_rate: float | None = None
    """[ZBEX] Discharge rate (output power) in percentage of maxP. (Unit: PerCent)"""

    reserve_percent: float | None = None
    """
    [ZBEX] 
    Percentage of the rated storage capacity that should be reserved during normal operations. This reserve acts as a safeguard, preventing the energy level 
    from dropping below this threshold under standard conditions. The field must be set to a non-negative value between 0 and 1. (Unit: PerCent)
    """

    control_mode: BatteryControlMode = BatteryControlMode.UNKNOWN
    """[ZBEX] Mode of operation for the dispatch (charging/discharging) function of BatteryControl."""
