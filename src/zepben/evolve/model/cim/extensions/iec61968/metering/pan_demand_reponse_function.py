#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from zepben.evolve.model.cim.iec61968.metering.ControlledAppliance import ControlledAppliance
from zepben.evolve.model.cim.iec61968.metering.metering import EndDeviceFunction, EndDeviceFunctionKind

if TYPE_CHECKING:
    pass

from zepben.evolve.util import require

__all__ = ["PanDemandResponseFunction"]


class PanDemandResponseFunction(EndDeviceFunction):
    """
    [ZBEX] PAN function that an end device supports, distinguished by 'kind'.
    """

    kind: EndDeviceFunctionKind = EndDeviceFunctionKind.UNKNOWN
    """`zepben.evolve.model.cim.iec61968.metering.metering.EndDeviceFunctionKind` of this `PanDemandResponseFunction`"""

    _appliance: Optional[int] = None

    def __init__(self, appliance: Optional[int] = None, **kwargs):
        super(EndDeviceFunction, self).__init__(**kwargs)
        if appliance:
            self._appliance = appliance

    def assign_controlled_appliance_configuration_bitmask(self, ca: int) -> PanDemandResponseFunction:
        """
        assign a `ControlledAppliance` configuration to this `PanDemandResponseFunction`.

        `ca` the bitmask value of the `ControlledAppliance` configuration.
        Raises `ValueError` if there is already an assigned `ControlledAppliance` configuration.
        """
        require(self._appliance is None, lambda: f"A ControlledAppliance configuration if already assigned to {str(self)}")

        self._appliance = ca
        return self

    def assign_controlled_appliance(self, ca: ControlledAppliance) -> PanDemandResponseFunction:
        """
        assign a `ControlledAppliance` configuration to this `PanDemandResponseFunction`.

        `ca` the `ControlledAppliance` being assigned to this `PanDemandResponseFunction`.
        Raises `ValueError` if there is already an assigned `ControlledAppliance` configuration.
        """
        require(self._appliance is None, lambda: f"A ControlledAppliance configuration if already assigned to {str(self)}")

        self._appliance = ca.to_int()
        return self

    def assign_controlled_appliance_configuration_individually(
        self,
        is_electric_vehicle: bool,
        is_exterior_lighting: bool,
        is_generation_system: bool,
        is_hvac_compressor_or_furnace: bool,
        is_interior_lighting: bool,
        is_irrigation_pump: bool,
        is_managed_commercial_industrial_load: bool,
        is_pool_pump_spa_jacuzzi: bool,
        is_simple_misc_load: bool,
        is_smart_appliance: bool,
        is_strip_and_baseboard_heater: bool,
        is_water_heater: bool,
    ) -> PanDemandResponseFunction:
        """
        Assign a `ControlledAppliance` configuration to this `PanDemandResponseFunction`.

        `is_electric_vehicle` True if the appliance is an electric vehicle
        `is_exterior_lighting` True if the appliance is exterior lighting
        `is_generation_system` True if the appliance is a generation system
        `is_hvac_compressor_or_furnace` True if the appliance is HVAC compressor or furnace
        `is_interior_lighting` True if the appliance is interior lighting
        `is_irrigation_pump` True if the appliance is an irrigation pump
        `is_managed_commercial_industrial_load` True if the appliance is managed commercial or industrial load
        `is_pool_pump_spa_jacuzzi` True if the appliance is a pool, pump, spa or jacuzzi
        `is_simple_misc_load` True if the appliance is a simple miscellaneous load
        `is_smart_appliance` True if the appliance is a smart appliance
        `is_strip_and_baseboard_heater` True if the appliance is a strip or baseboard heater
        `is_water_heater` True if the appliance is a water heater
        Raises `ValueError` if there is already an assigned `ControlledAppliance` configuration.
        """
        require(self._appliance is None, lambda: f"A ControlledAppliance configuration if already assigned to {str(self)}")

        self._appliance = self._appliance = ControlledAppliance([
            is_electric_vehicle,
            is_exterior_lighting,
            is_generation_system,
            is_hvac_compressor_or_furnace,
            is_interior_lighting,
            is_irrigation_pump,
            is_managed_commercial_industrial_load,
            is_pool_pump_spa_jacuzzi,
            is_simple_misc_load,
            is_smart_appliance,
            is_strip_and_baseboard_heater,
            is_water_heater
        ]).to_int()
        return self

    @property
    def appliance(self) -> Optional[ControlledAppliance]:
        """
        The `ControlledAppliance`s of this `PanDemandResponseFunction`.
        """
        if self._appliance is None:
            return None
        else:
            return ControlledAppliance.from_int(self._appliance)

    def update_appliance(
        self,
        is_electric_vehicle: Optional[bool] = None,
        is_exterior_lighting: Optional[bool] = None,
        is_generation_system: Optional[bool] = None,
        is_hvac_compressor_or_furnace: Optional[bool] = None,
        is_interior_lighting: Optional[bool] = None,
        is_irrigation_pump: Optional[bool] = None,
        is_managed_commercial_industrial_load: Optional[bool] = None,
        is_pool_pump_spa_jacuzzi: Optional[bool] = None,
        is_simple_misc_load: Optional[bool] = None,
        is_smart_appliance: Optional[bool] = None,
        is_strip_and_baseboard_heater: Optional[bool] = None,
        is_water_heater: Optional[bool] = None,
    ) -> PanDemandResponseFunction:
        """
        Update `ControlledAppliance` configuration to this `PanDemandResponseFunction`.

        `is_electric_vehicle` True if the appliance is an electric vehicle
        `is_exterior_lighting` True if the appliance is exterior lighting
        `is_generation_system` True if the appliance is a generation system
        `is_hvac_compressor_or_furnace` True if the appliance is HVAC compressor or furnace
        `is_interior_lighting` True if the appliance is interior lighting
        `is_irrigation_pump` True if the appliance is an irrigation pump
        `is_managed_commercial_industrial_load` True if the appliance is managed commercial or industrial load
        `is_pool_pump_spa_jacuzzi` True if the appliance is a pool, pump, spa or jacuzzi
        `is_simple_misc_load` True if the appliance is a simple miscellaneous load
        `is_smart_appliance` True if the appliance is a smart appliance
        `is_strip_and_baseboard_heater` True if the appliance is a strip or baseboard heater
        `is_water_heater` True if the appliance is a water heater
        Raises `ValueError` if there isn't already an assigned `ControlledAppliance` configuration.
        """
        require(self._appliance is not None, lambda: f"A ControlledAppliance configuration must first be assigned to {str(self)} before it can be updated.")

        received_config = {
            "is_electric_vehicle": is_electric_vehicle,
            "is_exterior_lighting": is_exterior_lighting,
            "is_generation_system": is_generation_system,
            "is_hvac_compressor_or_furnace": is_hvac_compressor_or_furnace,
            "is_interior_lighting": is_interior_lighting,
            "is_irrigation_pump": is_irrigation_pump,
            "is_managed_commercial_industrial_load": is_managed_commercial_industrial_load,
            "is_pool_pump_spa_jacuzzi": is_pool_pump_spa_jacuzzi,
            "is_simple_misc_load": is_simple_misc_load,
            "is_smart_appliance": is_smart_appliance,
            "is_strip_and_baseboard_heater": is_strip_and_baseboard_heater,
            "is_water_heater": is_water_heater,
        }
        current_appliance_config = self.appliance
        final_config = []
        for entry in received_config:
            if received_config[entry] is not None:
                final_config.append(received_config[entry])
            else:
                final_config.append(current_appliance_config.__getattribute__(entry))

        self._appliance = ControlledAppliance(final_config).to_int()
        return self

    def clear_appliance(self) -> PanDemandResponseFunction:
        self._appliance = None
        return self
