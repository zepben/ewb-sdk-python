#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["BatteryUnit"]

from typing import List, Optional, Generator, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.extensions.iec61970.base.wires.battery_control_mode import BatteryControlMode
from zepben.ewb.model.cim.iec61970.base.generation.production.battery_state_kind import BatteryStateKind
from zepben.ewb.model.cim.iec61970.base.generation.production.power_electronics_unit import PowerElectronicsUnit
from zepben.ewb.util import nlen, ngen, get_by_mrid, safe_remove

if TYPE_CHECKING:
    from zepben.ewb.model.cim.extensions.iec61970.base.wires.battery_control import BatteryControl


@dataslot
@boilermaker
class BatteryUnit(PowerElectronicsUnit):
    """An electrochemical energy storage device."""

    battery_state: BatteryStateKind = BatteryStateKind.UNKNOWN
    """The current state of the battery (charging, full, etc.)."""

    rated_e: int | None = None
    """Full energy storage capacity of the battery in watt hours (Wh). The attribute shall be a positive value."""

    stored_e: int | None = None
    """Amount of energy currently stored in watt hours (Wh). The attribute shall be a positive value or zero and lower than `rated_e`."""

    controls: List['BatteryControl'] | None = MRIDListAccessor()

    def _retype(self):
        self.controls: MRIDListRouter = ...

    # NOTE: This is called `num_battery_controls` because `num_controls` is already used by `PowerSystemResource`.
    @deprecated("BOILERPLATE: Use len(controls) instead")
    def num_battery_controls(self):
        """
        Returns The number of `BatteryControl`s associated with this `BatteryUnit`
        """
        return len(self.controls)

    @deprecated("BOILERPLATE: Use controls.get_by_mrid(mrid) instead")
    def get_control(self, mrid: str) -> 'BatteryControl':
        """
        Get the `BatteryControl` for this `BatteryUnit` identified by `mrid`

        `mrid` the mRID of the required `BatteryControl`
        Returns The `BatteryControl` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return self.controls.get_by_mrid(mrid)

    def get_control_by_mode(self, control_mode: BatteryControlMode) -> 'BatteryControl':
        """
        Get the `BatteryControl` for this `BatteryUnit` identified by its `control_mode`

        `control_mode` the `BatteryControlMode` of the desired `BatteryControl`
        Returns The `BatteryControl` with the specified `control_mode` if it exists
        Raises `KeyError` if a `BatteryControl` with `control_mode` wasn't present.
        """
        for control in self.controls:
            if control.control_mode == control_mode:
                return control
        raise IndexError(f"No BatteryControl with a control_mode of {control_mode} was found in BatteryUnit {str(self)}")

    @deprecated("BOILERPLATE: Use controls.append(bc) instead")
    def add_control(self, bc: 'BatteryControl') -> 'BatteryUnit':
        """
        Associate `bc` to this `BatteryUnit`.

        `bc` the `BatteryControl` to associate with this `BatteryUnit`.
        Returns A reference to this `BatteryUnit` to allow fluent use.
        Raises `ValueError` if another `BatteryControl` with the same `mrid` already exists for this `BatteryUnit`.
        """
        self.controls.append(bc)
        return self

    @deprecated("BOILERPLATE: Use controls.remove(bc) instead")
    def remove_control(self, bc: 'BatteryControl') -> 'BatteryUnit':
        """
        Disassociate `bc` from this `BatteryUnit`

        `bc` the `BatteryControl` to disassociate from this `BatteryUnit`.
        Returns A reference to this `BatteryUnit` to allow fluent use.
        Raises `ValueError` if `up` was not associated with this `BatteryUnit`.
        """
        self.controls.remove(bc)
        return self

    @deprecated("BOILERPLATE: Use controls.clear() instead")
    def clear_controls(self) -> 'BatteryUnit':
        """
        Clear all battery_controls.
        Returns A reference to this `BatteryUnit` to allow fluent use.
        """
        self.controls.clear()
        return self
