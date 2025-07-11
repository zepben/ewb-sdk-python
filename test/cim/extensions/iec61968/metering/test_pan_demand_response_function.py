#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from pytest import raises
from hypothesis import given
from hypothesis.strategies import sampled_from, integers

from cim.iec61968.metering.test_end_device_function import end_device_function_kwargs, end_device_function_args, verify_end_device_function_constructor_default, \
    verify_end_device_function_constructor_args
from test.cim.iec61968.metering.test_end_device_function import verify_end_device_function_constructor_kwargs
from zepben.ewb import PanDemandResponseFunction, ControlledAppliance, Appliance
from zepben.ewb.model.cim.iec61968.metering.end_device_function_kind import EndDeviceFunctionKind

pan_demand_response_function_kwargs = {
    **end_device_function_kwargs,
    "kind": sampled_from(EndDeviceFunctionKind),
    "appliance": integers(min_value=0, max_value=4095)
}

pan_demand_response_function_args = [*end_device_function_args, EndDeviceFunctionKind.demandResponse, 1]


def test_pan_demand_response_function_constructor_default():
    pdrf = PanDemandResponseFunction()

    verify_end_device_function_constructor_default(pdrf)

    assert pdrf.kind is EndDeviceFunctionKind.UNKNOWN
    assert pdrf.appliance is None


@given(**pan_demand_response_function_kwargs)
def test_pan_demand_response_function_constructor_kwargs(kind, appliance, **kwargs):
    pdrf = PanDemandResponseFunction(kind=kind, appliances=appliance, **kwargs)

    verify_end_device_function_constructor_kwargs(pdrf, **kwargs)
    assert pdrf.kind == kind
    assert pdrf.appliance.bitmask == appliance


def test_pan_demand_response_function_constructor_args():
    pdrf = PanDemandResponseFunction(*pan_demand_response_function_args)

    verify_end_device_function_constructor_args(pdrf)

    assert pan_demand_response_function_args[-2:] == [pdrf.kind, pdrf.appliance.bitmask]


def test_constructor_with_controlled_appliance():
    ca = ControlledAppliance([Appliance.SMART_APPLIANCE, Appliance.IRRIGATION_PUMP])
    pdrf = PanDemandResponseFunction(appliances=ca)

    assert pdrf.appliance == ca


def test_appliance_setter():
    ca = ControlledAppliance([Appliance.SMART_APPLIANCE, Appliance.IRRIGATION_PUMP])
    pdrf = PanDemandResponseFunction()
    pdrf.appliance = ca
    assert pdrf.appliance == ca

    pdrf.appliance = None
    assert pdrf.appliance is None


def test_add_remove_appliances():
    pdrf = PanDemandResponseFunction()

    assert pdrf.add_appliance(Appliance.WATER_HEATER), "should have added"
    validate_appliance(pdrf.appliance, is_water_heater=True)
    assert pdrf.add_appliance(Appliance.ELECTRIC_VEHICLE), "should have added"
    validate_appliance(pdrf.appliance, is_water_heater=True, is_electric_vehicle=True)

    assert not pdrf.add_appliance(Appliance.ELECTRIC_VEHICLE), "shouldn't have added"
    validate_appliance(pdrf.appliance, is_water_heater=True, is_electric_vehicle=True)

    assert pdrf.remove_appliance(Appliance.WATER_HEATER), "should have removed"
    validate_appliance(pdrf.appliance, is_electric_vehicle=True)

    assert not pdrf.remove_appliance(Appliance.WATER_HEATER), "shouldn't have removed unused"
    validate_appliance(pdrf.appliance, is_electric_vehicle=True)

    assert pdrf.remove_appliance(Appliance.ELECTRIC_VEHICLE), "should have removed"
    validate_appliance(pdrf.appliance)


def test_add_remove_multiple_appliances():
    pdrf = PanDemandResponseFunction()

    with raises(ValueError, match="You must provide at least one appliance to add"):
        pdrf.add_appliances([])

    # Add appliance with no previous bitmask
    assert pdrf.add_appliances([Appliance.SMART_APPLIANCE, Appliance.IRRIGATION_PUMP]), "should have added"
    validate_appliance(pdrf.appliance, is_smart_appliance=True, is_irrigation_pump=True)

    # Add partial duplicate appliance with a previous bitmask
    assert pdrf.add_appliances([Appliance.ELECTRIC_VEHICLE, Appliance.IRRIGATION_PUMP]), "should have added"
    validate_appliance(pdrf.appliance, is_smart_appliance=True, is_irrigation_pump=True, is_electric_vehicle=True)

    # Add duplicate appliances
    assert not pdrf.add_appliances([Appliance.ELECTRIC_VEHICLE, Appliance.IRRIGATION_PUMP]), "shouldn't have added"
    validate_appliance(pdrf.appliance, is_smart_appliance=True, is_irrigation_pump=True, is_electric_vehicle=True)

    # Must include appliances to remove
    with raises(ValueError, match="You must provide at least one appliance to remove"):
        pdrf.remove_appliances([])

    # Remove appliance with a remaining bitmask
    assert pdrf.remove_appliances([Appliance.ELECTRIC_VEHICLE, Appliance.IRRIGATION_PUMP]), "should have removed"
    validate_appliance(pdrf.appliance, is_smart_appliance=True)

    # Remove appliance that wasn't included
    assert not pdrf.remove_appliances([Appliance.ELECTRIC_VEHICLE, Appliance.IRRIGATION_PUMP]), "shouldn't have removed"
    validate_appliance(pdrf.appliance, is_smart_appliance=True)

    # Remove partial unused appliances with no remaning bitmask.
    assert pdrf.remove_appliances([Appliance.SMART_APPLIANCE, Appliance.IRRIGATION_PUMP]), "should have removed"
    validate_appliance(pdrf.appliance)


def test_remove_appliance_initialises_bitmask():
    pdrf = PanDemandResponseFunction()
    assert pdrf._appliance_bitmask is None
    assert pdrf.appliance is None

    assert pdrf.remove_appliance(Appliance.ELECTRIC_VEHICLE), "shouldn't have removed"
    assert pdrf._appliance_bitmask == 0
    validate_appliance(pdrf.appliance)


def test_removing_appliances_initialises_bitmask():
    pdrf = PanDemandResponseFunction()
    assert pdrf._appliance_bitmask is None
    assert pdrf.appliance is None

    assert pdrf.remove_appliances([Appliance.ELECTRIC_VEHICLE]), "shouldn't have removed"
    assert pdrf._appliance_bitmask == 0
    validate_appliance(pdrf.appliance)


def validate_appliance(controlled_appliance: ControlledAppliance,
                       is_electric_vehicle: bool = False,
                       is_exterior_lighting: bool = False,
                       is_generation_system: bool = False,
                       is_hvac_compressor_or_furnace: bool = False,
                       is_interior_lighting: bool = False,
                       is_irrigation_pump: bool = False,
                       is_managed_commercial_industrial_load: bool = False,
                       is_pool_pump_spa_jacuzzi: bool = False,
                       is_simple_misc_load: bool = False,
                       is_smart_appliance: bool = False,
                       is_strip_and_baseboard_heater: bool = False,
                       is_water_heater: bool = False):
    assert controlled_appliance is not None
    assert controlled_appliance.is_electric_vehicle == is_electric_vehicle
    assert controlled_appliance.is_exterior_lighting == is_exterior_lighting
    assert controlled_appliance.is_generation_system == is_generation_system
    assert controlled_appliance.is_hvac_compressor_or_furnace == is_hvac_compressor_or_furnace
    assert controlled_appliance.is_interior_lighting == is_interior_lighting
    assert controlled_appliance.is_irrigation_pump == is_irrigation_pump
    assert controlled_appliance.is_managed_commercial_industrial_load == is_managed_commercial_industrial_load
    assert controlled_appliance.is_pool_pump_spa_jacuzzi == is_pool_pump_spa_jacuzzi
    assert controlled_appliance.is_simple_misc_load == is_simple_misc_load
    assert controlled_appliance.is_smart_appliance == is_smart_appliance
    assert controlled_appliance.is_strip_and_baseboard_heater == is_strip_and_baseboard_heater
    assert controlled_appliance.is_water_heater == is_water_heater
