#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional

from zepben.evolve.model.cim.iec61970.base.core.equipment import Equipment
from zepben.evolve.model.cim.iec61970.base.wires.generation.production.battery_state_kind import BatteryStateKind
from zepben.evolve.model.cim.iec61970.base.wires.power_electronics_connection import PowerElectronicsConnection


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

    battery_state: BatteryStateKind = BatteryStateKind.UNKNOWN
    """The current state of the battery (charging, full, etc.)."""

    rated_e: Optional[int] = None
    """Full energy storage capacity of the battery in watt hours (Wh). The attribute shall be a positive value."""

    stored_e: Optional[int] = None
    """Amount of energy currently stored in watt hours (Wh). The attribute shall be a positive value or zero and lower than `rated_e`."""


class PowerElectronicsWindUnit(PowerElectronicsUnit):
    """A wind generating unit that connects to the AC network with power electronics rather than rotating machines or an aggregation of such units."""
    pass


class PhotoVoltaicUnit(PowerElectronicsUnit):
    """A photovoltaic device or an aggregation of such devices."""
    pass
