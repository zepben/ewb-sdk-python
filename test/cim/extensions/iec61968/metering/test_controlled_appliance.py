#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import ControlledAppliance, Appliance


def test_constructor_with_appliances():
    for app in Appliance:
        ca = ControlledAppliance(app)
        assert ControlledAppliance(app).bitmask == ca.bitmask

    ca = ControlledAppliance([Appliance.ELECTRIC_VEHICLE, Appliance.EXTERIOR_LIGHTING, Appliance.INTERIOR_LIGHTING])
    assert Appliance.ELECTRIC_VEHICLE.bitmask | Appliance.EXTERIOR_LIGHTING.bitmask | Appliance.INTERIOR_LIGHTING.bitmask == ca.bitmask


def test_constructor_with_bitmask():
    # Bitmask of zero should exclude all types
    validate_bitmask_constructor(0)

    # Each bit controls a different field
    validate_bitmask_constructor(Appliance.ELECTRIC_VEHICLE.bitmask, expect_is_electric_vehicle=True)
    validate_bitmask_constructor(Appliance.EXTERIOR_LIGHTING.bitmask, expect_is_exterior_lighting=True)
    validate_bitmask_constructor(Appliance.GENERATION_SYSTEM.bitmask, expect_is_generation_system=True)
    validate_bitmask_constructor(Appliance.HVAC_COMPRESSOR_OR_FURNACE.bitmask, expect_is_hvac_compressor_or_furnace=True)
    validate_bitmask_constructor(Appliance.INTERIOR_LIGHTING.bitmask, expect_is_interior_lighting=True)
    validate_bitmask_constructor(Appliance.IRRIGATION_PUMP.bitmask, expect_is_irrigation_pump=True)
    validate_bitmask_constructor(Appliance.MANAGED_COMMERCIAL_INDUSTRIAL_LOAD.bitmask, expect_is_managed_commercial_industrial_load=True)
    validate_bitmask_constructor(Appliance.POOL_PUMP_SPA_JACUZZI.bitmask, expect_is_pool_pump_spa_jacuzzi=True)
    validate_bitmask_constructor(Appliance.SIMPLE_MISC_LOAD.bitmask, expect_is_simple_misc_load=True)
    validate_bitmask_constructor(Appliance.SMART_APPLIANCE.bitmask, expect_is_smart_appliance=True)
    validate_bitmask_constructor(Appliance.STRIP_AND_BASEBOARD_HEATER.bitmask, expect_is_strip_and_baseboard_heater=True)
    validate_bitmask_constructor(Appliance.WATER_HEATER.bitmask, expect_is_water_heater=True)

    # Can combine more than one
    validate_bitmask_constructor(Appliance.ELECTRIC_VEHICLE.bitmask | Appliance.EXTERIOR_LIGHTING.bitmask, expect_is_electric_vehicle=True, expect_is_exterior_lighting=True)


def validate_bitmask_constructor(bitmask: int,
                                 expect_is_electric_vehicle: bool = False,
                                 expect_is_exterior_lighting: bool = False,
                                 expect_is_generation_system: bool = False,
                                 expect_is_hvac_compressor_or_furnace: bool = False,
                                 expect_is_interior_lighting: bool = False,
                                 expect_is_irrigation_pump: bool = False,
                                 expect_is_managed_commercial_industrial_load: bool = False,
                                 expect_is_pool_pump_spa_jacuzzi: bool = False,
                                 expect_is_simple_misc_load: bool = False,
                                 expect_is_smart_appliance: bool = False,
                                 expect_is_strip_and_baseboard_heater: bool = False,
                                 expect_is_water_heater: bool = False):
    ca = ControlledAppliance(bitmask)
    assert ca.is_electric_vehicle == expect_is_electric_vehicle
    assert ca.is_exterior_lighting == expect_is_exterior_lighting
    assert ca.is_generation_system == expect_is_generation_system
    assert ca.is_hvac_compressor_or_furnace == expect_is_hvac_compressor_or_furnace
    assert ca.is_interior_lighting == expect_is_interior_lighting
    assert ca.is_irrigation_pump == expect_is_irrigation_pump
    assert ca.is_managed_commercial_industrial_load == expect_is_managed_commercial_industrial_load
    assert ca.is_pool_pump_spa_jacuzzi == expect_is_pool_pump_spa_jacuzzi
    assert ca.is_simple_misc_load == expect_is_simple_misc_load
    assert ca.is_smart_appliance == expect_is_smart_appliance
    assert ca.is_strip_and_baseboard_heater == expect_is_strip_and_baseboard_heater
    assert ca.is_water_heater == expect_is_water_heater
