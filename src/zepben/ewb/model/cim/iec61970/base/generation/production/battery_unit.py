#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["BatteryUnit"]

from typing import List, Optional, Generator, TYPE_CHECKING

from zepben.ewb.model.cim.extensions.iec61970.base.wires.battery_control_mode import BatteryControlMode
from zepben.ewb.model.cim.iec61970.base.generation.production.battery_state_kind import BatteryStateKind
from zepben.ewb.model.cim.iec61970.base.generation.production.power_electronics_unit import PowerElectronicsUnit
from zepben.ewb.util import nlen, ngen, get_by_mrid, safe_remove

if TYPE_CHECKING:
    from zepben.ewb.model.cim.extensions.iec61970.base.wires.battery_control import BatteryControl


class BatteryUnit(PowerElectronicsUnit):
    """An electrochemical energy storage device."""

    def __init__(self, controls: List['BatteryControl'] = None, **kwargs):
        super(BatteryUnit, self).__init__(**kwargs)
        if controls:
            for bc in controls:
                self.add_control(bc)

    battery_state: BatteryStateKind = BatteryStateKind.UNKNOWN
    """The current state of the battery (charging, full, etc.)."""

    rated_e: Optional[int] = None
    """Full energy storage capacity of the battery in watt hours (Wh). The attribute shall be a positive value."""

    stored_e: Optional[int] = None
    """Amount of energy currently stored in watt hours (Wh). The attribute shall be a positive value or zero and lower than `rated_e`."""

    _controls: Optional[List['BatteryControl']] = None

    # NOTE: This is called `num_battery_controls` because `num_controls` is already used by `PowerSystemResource`.
    def num_battery_controls(self):
        """
        Returns The number of `BatteryControl`s associated with this `BatteryUnit`
        """
        return nlen(self._controls)

    @property
    def controls(self) -> Generator['BatteryControl', None, None]:
        """
        [ZBEX] The `BatteryControl`s associated with this `BatteryUnit`
        """
        return ngen(self._controls)

    def get_control(self, mrid: str) -> 'BatteryControl':
        """
        Get the `BatteryControl` for this `BatteryUnit` identified by `mrid`

        `mrid` the mRID of the required `BatteryControl`
        Returns The `BatteryControl` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._controls, mrid)

    def get_control_by_mode(self, control_mode: BatteryControlMode) -> 'BatteryControl':
        """
        Get the `BatteryControl` for this `BatteryUnit` identified by its `control_mode`

        `control_mode` the `BatteryControlMode` of the desired `BatteryControl`
        Returns The `BatteryControl` with the specified `control_mode` if it exists
        Raises `KeyError` if a `BatteryControl` with `control_mode` wasn't present.
        """
        if self._controls:
            for control in self._controls:
                if control.control_mode == control_mode:
                    return control
        raise IndexError(f"No BatteryControl with a control_mode of {control_mode} was found in BatteryUnit {str(self)}")

    def add_control(self, bc: 'BatteryControl') -> 'BatteryUnit':
        """
        Associate `bc` to this `BatteryUnit`.

        `bc` the `BatteryControl` to associate with this `BatteryUnit`.
        Returns A reference to this `BatteryUnit` to allow fluent use.
        Raises `ValueError` if another `BatteryControl` with the same `mrid` already exists for this `BatteryUnit`.
        """
        if self._validate_reference(bc, self.get_control, "A BatteryControl"):
            return self
        self._controls = list() if self._controls is None else self._controls
        self._controls.append(bc)
        return self

    def remove_control(self, bc: 'BatteryControl') -> 'BatteryUnit':
        """
        Disassociate `bc` from this `BatteryUnit`

        `bc` the `BatteryControl` to disassociate from this `BatteryUnit`.
        Returns A reference to this `BatteryUnit` to allow fluent use.
        Raises `ValueError` if `up` was not associated with this `BatteryUnit`.
        """
        self._controls = safe_remove(self._controls, bc)
        return self

    def clear_controls(self) -> 'BatteryUnit':
        """
        Clear all battery_controls.
        Returns A reference to this `BatteryUnit` to allow fluent use.
        """
        self._controls = None
        return self
