#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["BatteryUnit"]

from typing import List, Optional, TYPE_CHECKING
from dataclasses import field
from typing_extensions import deprecated

from zepben.ewb.model.cim.extensions.iec61970.base.wires.battery_control_mode import BatteryControlMode
from zepben.ewb.model.cim.iec61970.base.generation.production.battery_state_kind import BatteryStateKind
from zepben.ewb.model.cim.iec61970.base.generation.production.power_electronics_unit import PowerElectronicsUnit
from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb.boilerplate.relations.battery_control_list import BatteryControlList

if TYPE_CHECKING:
    from zepben.ewb.model.cim.extensions.iec61970.base.wires.battery_control import BatteryControl


@zb_dataclass
class BatteryUnit(PowerElectronicsUnit):
    """An electrochemical energy storage device."""

    battery_state: BatteryStateKind = BatteryStateKind.UNKNOWN
    """The current state of the battery (charging, full, etc.)."""

    rated_e: Optional[int] = None
    """Full energy storage capacity of the battery in watt hours (Wh). The attribute shall be a positive value."""

    stored_e: Optional[int] = None
    """Amount of energy currently stored in watt hours (Wh). The attribute shall be a positive value or zero and lower than `rated_e`."""

    _controls: Optional[List['BatteryControl']] = field(default=None)

    # NOTE: This is called `num_battery_controls` because `num_controls` is already used by `PowerSystemResource`.

    controls: BatteryControlList['BatteryControl'] = BatteryControlList(
        _controls,
        "A BatteryControl",
    )


    # region deprecated list boilerplate
    # region controls boilerplate

    @deprecated("Use len(obj.controls) instead.")
    def num_battery_controls(self):
        return len(self.controls)

    @deprecated("Use obj.controls.get_by_mrid(mrid) instead.")
    def get_control(self, mrid: str) -> 'BatteryControl':
        return self.controls.get_by_mrid(mrid)

    @deprecated("Use obj.controls.get_by_mode(control_mode) instead.")
    def get_control_by_mode(self, control_mode: BatteryControlMode) -> 'BatteryControl':
        return self.controls.get_by_mode(control_mode)

    @deprecated("Use obj.controls.append(bc) instead.")
    def add_control(self, bc: 'BatteryControl') -> 'BatteryUnit':
        self.controls.append(bc)
        return self

    @deprecated("Use obj.controls.remove(bc) instead.")
    def remove_control(self, bc: 'BatteryControl') -> 'BatteryUnit':
        self.controls.remove(bc)
        return self

    @deprecated("Use obj.controls.clear() instead.")
    def clear_controls(self) -> 'BatteryUnit':
        self.controls.clear()
        return self

    # endregion controls boilerplate

    # endregion deprecated list boilerplate
