#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import logging
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    pass

__all__ = ["ControlledAppliance"]

logger = logging.getLogger(__name__)


class ControlledAppliance:
    """
    Appliance controlled with a PAN device control.
    """

    is_electric_vehicle: bool = False
    """True if the appliance is an electric vehicle"""

    is_exterior_lighting: bool = False
    """True if the appliance is exterior lighting"""

    is_generation_system: bool = False
    """True if the appliance is a generation system"""

    is_hvac_compressor_or_furnace: bool = False
    """True if the appliance is HVAC compressor or furnace"""

    is_interior_lighting: bool = False
    """True if the appliance is interior lighting"""

    is_irrigation_pump: bool = False
    """True if the appliance is an irrigation pump"""

    is_managed_commercial_industrial_load: bool = False
    """True if the appliance is managed commercial or industrial load"""

    is_pool_pump_spa_jacuzzi: bool = False
    """True if the appliance is a pool, pump, spa or jacuzzi"""

    is_simple_misc_load: bool = False
    """True if the appliance is a simple miscellaneous load"""

    is_smart_appliance: bool = False
    """True if the appliance is a smart appliance"""

    is_strip_and_baseboard_heater: bool = False
    """True if the appliance is a strip or baseboard heater"""

    is_water_heater: bool = False
    """True if the appliance is a water heater"""

    def __init__(self, configs: List[bool] = None, **kwargs):
        if configs:
            self.is_electric_vehicle = configs[0]
            self.is_exterior_lighting = configs[1]
            self.is_generation_system = configs[2]
            self.is_hvac_compressor_or_furnace = configs[3]
            self.is_interior_lighting = configs[4]
            self.is_irrigation_pump = configs[5]
            self.is_managed_commercial_industrial_load = configs[6]
            self.is_pool_pump_spa_jacuzzi = configs[7]
            self.is_simple_misc_load = configs[8]
            self.is_smart_appliance = configs[9]
            self.is_strip_and_baseboard_heater = configs[10]
            self.is_water_heater = configs[11]

    def to_int(self) -> int:
        result = 0
        for variable in [attr for attr in dir(ControlledAppliance) if not callable(getattr(ControlledAppliance, attr)) and not attr.startswith("__")]:
            if self.__getattribute__(variable):
                result += ControlledAppliance.bitmask(variable)
        return result

    @staticmethod
    def from_int(config: int):
        """
        Return a `ControlledAppliance`

        `config` the bitmask of configuration
        """
        variables = [attr for attr in dir(ControlledAppliance) if not callable(getattr(ControlledAppliance, attr)) and not attr.startswith("__")]

        decoded_result = list(map(ControlledAppliance.decode, variables, [config] * 12))

        return ControlledAppliance(decoded_result)

    @staticmethod
    def decode(variable_name: str, value: int) -> bool:
        """
        Decode the setting for a variable base on input Int
        """
        return value & ControlledAppliance.bitmask(variable_name) > 0

    @staticmethod
    def bitmask(variable_name: str) -> int:
        """
        Get the bitmask of a variable of a ControlledAppliance

        `variable_name` the name of the attribute
        Returns The bitmask of the given `variable_name`
        """
        match variable_name:
            case "is_electric_vehicle":
                return 1 << 0
            case "is_exterior_lighting":
                return 1 << 1
            case "is_generation_system":
                return 1 << 2
            case "is_hvac_compressor_or_furnace":
                return 1 << 3
            case "is_interior_lighting":
                return 1 << 4
            case "is_irrigation_pump":
                return 1 << 5
            case "is_managed_commercial_industrial_load":
                return 1 << 6
            case "is_pool_pump_spa_jacuzzi":
                return 1 << 7
            case "is_simple_misc_load":
                return 1 << 8
            case "is_smart_appliance":
                return 1 << 9
            case "is_strip_and_baseboard_heater":
                return 1 << 10
            case "is_water_heater":
                return 1 << 11
            case _:
                return -1
