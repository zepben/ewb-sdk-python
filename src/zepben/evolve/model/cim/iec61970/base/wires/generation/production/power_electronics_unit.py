#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional, List, Generator

from zepben.evolve.model.cim.extensions.iec61970.base.wires.battery_control import BatteryControl
from zepben.evolve.model.cim.iec61970.base.core.equipment import Equipment
from zepben.evolve.model.cim.iec61970.base.wires.generation.production.battery_state_kind import BatteryStateKind
from zepben.evolve.model.cim.iec61970.base.wires.power_electronics_connection import PowerElectronicsConnection
from zepben.evolve.util import nlen, get_by_mrid, ngen, safe_remove

__all__ = ["PowerElectronicsConnection", "BatteryUnit", "PowerElectronicsWindUnit", "PowerElectronicsUnit", "PhotoVoltaicUnit"]


class PowerElectronicsUnit(Equipment):
    """
    A generating unit or battery or aggregation that connects to the AC network using power electronics rather than rotating machines.
    """

    power_electronics_connection: Optional[PowerElectronicsConnection] = None
    """An AC network connection may have several power electronics units connecting through it."""

    max_p: Optional[int] = None
    """Maximum active power limit. This is the maximum (nameplate) limit for the unit."""

    min_p: Optional[int] = None
    """Minimum active power limit. This is the minimum (nameplate) limit for the unit."""


class BatteryUnit(PowerElectronicsUnit):
    """An electrochemical energy storage device."""

    def __init__(self, battery_controls: List[BatteryControl] = None, **kwargs):
        super(BatteryUnit, self).__init__(**kwargs)
        if battery_controls:
            for bc in battery_controls:
                self.add_battery_control(bc)

    battery_state: BatteryStateKind = BatteryStateKind.UNKNOWN
    """The current state of the battery (charging, full, etc.)."""

    rated_e: Optional[int] = None
    """Full energy storage capacity of the battery in watt hours (Wh). The attribute shall be a positive value."""

    stored_e: Optional[int] = None
    """Amount of energy currently stored in watt hours (Wh). The attribute shall be a positive value or zero and lower than `rated_e`."""

    _battery_controls: Optional[List[BatteryControl]] = None

    def num_battery_controls(self):
        """
        Returns The number of `BatteryControl`s associated with this `BatteryUnit`
        """
        return nlen(self._battery_controls)

    @property
    def battery_controls(self) -> Generator[BatteryControl, None, None]:
        """
        The `BatteryControl`s associated with this `BatteryUnit`
        """
        return ngen(self._battery_controls)

    def get_battery_control(self, mrid: str) -> BatteryControl:
        """
        Get the `BatteryControl` for this `BatteryUnit` identified by `mrid`

        `mrid` the mRID of the required `BatteryControl`
        Returns The `BatteryControl` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._battery_controls, mrid)

    def add_battery_control(self, edf: BatteryControl) -> 'BatteryUnit':
        """
        Associate `edf` to this `BatteryUnit`.

        `edf` the `BatteryControl` to associate with this `BatteryUnit`.
        Returns A reference to this `BatteryUnit` to allow fluent use.
        Raises `ValueError` if another `BatteryControl` with the same `mrid` already exists for this `BatteryUnit`.
        """
        if self._validate_reference(edf, self.get_battery_control, "An BatteryControl"):
            return self
        self._battery_controls = list() if self._battery_controls is None else self._battery_controls
        self._battery_controls.append(edf)
        return self

    def remove_battery_control(self, edf: BatteryControl) -> 'BatteryUnit':
        """
        Disassociate `edf` from this `BatteryUnit`

        `up` the `BatteryControl` to disassociate from this `BatteryUnit`.
        Returns A reference to this `BatteryUnit` to allow fluent use.
        Raises `ValueError` if `up` was not associated with this `BatteryUnit`.
        """
        self._battery_controls = safe_remove(self._battery_controls, edf)
        return self

    def clear_battery_controls(self) -> 'BatteryUnit':
        """
        Clear all battery_controls.
        Returns A reference to this `BatteryUnit` to allow fluent use.
        """
        self._battery_controls = None
        return self


class PowerElectronicsWindUnit(PowerElectronicsUnit):
    """A wind generating unit that connects to the AC network with power electronics rather than rotating machines or an aggregation of such units."""
    pass


class PhotoVoltaicUnit(PowerElectronicsUnit):
    """A photovoltaic device or an aggregation of such devices."""
    pass
