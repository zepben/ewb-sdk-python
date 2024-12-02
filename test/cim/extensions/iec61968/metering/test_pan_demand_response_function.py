#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import sampled_from, integers

from cim.iec61968.metering.test_end_device_function import end_device_function_kwargs, end_device_function_args, \
    verify_end_device_function_constructor_default
from test.cim.iec61968.metering.test_end_device_function import verify_end_device_function_constructor_kwargs
from zepben.evolve import EndDeviceFunctionKind
from zepben.evolve.model.cim.extensions.iec61968.metering.pan_demand_reponse_function import PanDemandResponseFunction
from zepben.evolve.model.cim.iec61968.metering.ControlledAppliance import ControlledAppliance

pan_demand_response_function_kwargs = {
    **end_device_function_kwargs,
    "kind": sampled_from(EndDeviceFunctionKind),
    "appliance": integers(min_value=0, max_value=4095)
}

pan_demand_response_function_args = [*end_device_function_args, EndDeviceFunctionKind.demandResponse]


def test_pan_demand_response_function_constructor_default():
    pdrf = PanDemandResponseFunction()

    verify_end_device_function_constructor_default(pdrf)

    assert pdrf.kind is EndDeviceFunctionKind.UNKNOWN
    assert pdrf.appliance is None


@given(**pan_demand_response_function_kwargs)
def test_pan_demand_response_function_constructor_kwargs(
    kind,
    appliance,
    **kwargs):
    pdrf = PanDemandResponseFunction(
        kind=kind,
        **kwargs
    )

    verify_end_device_function_constructor_kwargs(pdrf, **kwargs)
    assert pdrf.kind == kind


def test_pan_demand_response_function_constructor_args():
    pdrf = PanDemandResponseFunction(*pan_demand_response_function_args)

    assert pan_demand_response_function_args[-1:] == [
        pdrf.kind
    ]


def test_pan_demand_response_function_assign_controlled_appliance_configuration_bitmask():
    pdrf = PanDemandResponseFunction(*pan_demand_response_function_args)

    pdrf.assign_controlled_appliance_configuration_bitmask(1234)

    assert pdrf.appliance.to_int() == 1234


def test_pan_demand_response_function_assign_controlled_appliance():
    pdrf = PanDemandResponseFunction(*pan_demand_response_function_args)
    ca = ControlledAppliance.from_int(1234)

    pdrf.assign_controlled_appliance(ca)

    assert pdrf.appliance.to_int() == ca.to_int()


def test_pan_demand_response_function_assign_controlled_appliance_configuration_individually():
    pdrf = PanDemandResponseFunction(*pan_demand_response_function_args)

    pdrf.assign_controlled_appliance_configuration_individually(
        False,
        True,
        False,
        False,
        True,
        False,
        True,
        True,
        False,
        False,
        True,
        False
    )

    assert pdrf.appliance.to_int() == 1234


def test_pan_demand_response_function_update_appliance():
    pdrf = PanDemandResponseFunction(*pan_demand_response_function_args)

    pdrf.assign_controlled_appliance_configuration_bitmask(1234)
    pdrf.update_appliance(
        is_electric_vehicle=True
    )

    assert pdrf.appliance.to_int() == 1235


def test_pan_demand_response_function_clear_appliance():
    pdrf = PanDemandResponseFunction(*pan_demand_response_function_args)

    pdrf.assign_controlled_appliance_configuration_bitmask(1234)
    pdrf.clear_appliance()

    assert pdrf.appliance is None
