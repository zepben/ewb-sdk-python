#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum
from typing import List, TYPE_CHECKING, Union

if TYPE_CHECKING:
    pass

__all__ = ["ControlledAppliance", "Appliance"]

logger = logging.getLogger(__name__)


class Appliance(Enum):
    ELECTRIC_VEHICLE = 0
    EXTERIOR_LIGHTING = 1
    GENERATION_SYSTEM = 2
    HVAC_COMPRESSOR_OR_FURNACE = 3
    INTERIOR_LIGHTING = 4
    IRRIGATION_PUMP = 5
    MANAGED_COMMERCIAL_INDUSTRIAL_LOAD = 6
    POOL_PUMP_SPA_JACUZZI = 7
    SIMPLE_MISC_LOAD = 8
    SMART_APPLIANCE = 9
    STRIP_AND_BASEBOARD_HEATER = 10
    WATER_HEATER = 11

    @property
    def bitmask(self):
        return 1 << self.value


@dataclass
class ControlledAppliance:
    """
    Appliance controlled with a PAN device control.
    """

    _bitmask: int

    def __init__(self, appliances: Union[int, Appliance, List[Appliance]]):
        if isinstance(appliances, int):
            self._bitmask = appliances
        elif isinstance(appliances, Appliance):
            self._bitmask = appliances.bitmask
        elif isinstance(appliances, List):
            if appliances:
                def f(bitmask: int, nxt: Appliance) -> int:
                    return bitmask | nxt.bitmask

                acc = appliances[0].bitmask
                if len(appliances) > 1:
                    _ = [acc := f(acc, app) for app in appliances[1:]]
                self._bitmask = acc

    @property
    def bitmask(self):
        return self._bitmask

    @property
    def is_electric_vehicle(self) -> bool:
        """True if the appliance is an electric vehicle"""
        return Appliance.ELECTRIC_VEHICLE in self

    @property
    def is_exterior_lighting(self) -> bool:
        """True if the appliance is exterior lighting"""
        return Appliance.EXTERIOR_LIGHTING in self

    @property
    def is_generation_system(self) -> bool:
        """True if the appliance is a generation system"""
        return Appliance.GENERATION_SYSTEM in self

    @property
    def is_hvac_compressor_or_furnace(self) -> bool:
        """True if the appliance is HVAC compressor or furnace"""
        return Appliance.HVAC_COMPRESSOR_OR_FURNACE in self

    @property
    def is_interior_lighting(self) -> bool:
        """True if the appliance is interior lighting"""
        return Appliance.INTERIOR_LIGHTING in self

    @property
    def is_irrigation_pump(self) -> bool:
        """True if the appliance is an irrigation pump"""
        return Appliance.IRRIGATION_PUMP in self

    @property
    def is_managed_commercial_industrial_load(self) -> bool:
        """True if the appliance is managed commercial or industrial load"""
        return Appliance.MANAGED_COMMERCIAL_INDUSTRIAL_LOAD in self

    @property
    def is_pool_pump_spa_jacuzzi(self) -> bool:
        """True if the appliance is a pool, pump, spa or jacuzzi"""
        return Appliance.POOL_PUMP_SPA_JACUZZI in self

    @property
    def is_simple_misc_load(self) -> bool:
        """True if the appliance is a simple miscellaneous load"""
        return Appliance.SIMPLE_MISC_LOAD in self

    @property
    def is_smart_appliance(self) -> bool:
        """True if the appliance is a smart appliance"""
        return Appliance.SMART_APPLIANCE in self

    @property
    def is_strip_and_baseboard_heater(self) -> bool:
        """True if the appliance is a strip or baseboard heater"""
        return Appliance.STRIP_AND_BASEBOARD_HEATER in self

    @property
    def is_water_heater(self) -> bool:
        """True if the appliance is a water heater"""
        return Appliance.WATER_HEATER in self

    def __contains__(self, item: Appliance):
        return (self._bitmask & item.bitmask) != 0
