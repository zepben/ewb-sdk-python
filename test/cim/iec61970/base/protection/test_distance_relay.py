#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest
from hypothesis import given
from hypothesis.strategies import floats, booleans

from cim.cim_creators import FLOAT_MIN, FLOAT_MAX
from cim.iec61970.base.protection.test_protection_relay_function import protection_relay_function_kwargs, protection_relay_function_args, \
    verify_protection_relay_function_constructor_default, verify_protection_relay_function_constructor_kwargs, verify_protection_relay_function_constructor_args

from zepben.evolve import DistanceRelay

distance_relay_kwargs = {
    **protection_relay_function_kwargs,
    "backward_blind": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "backward_reach": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "backward_reactance": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "forward_blind": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "forward_reach": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "forward_reactance": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "operation_phase_angle1": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "operation_phase_angle2": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "operation_phase_angle3": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
}

distance_relay_args = [*protection_relay_function_args, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9]


def test_distance_relay_constructor_default():
    dr = DistanceRelay()

    verify_protection_relay_function_constructor_default(dr)
    assert dr.backward_blind is None
    assert dr.backward_reach is None
    assert dr.backward_reactance is None
    assert dr.forward_blind is None
    assert dr.forward_reach is None
    assert dr.forward_reactance is None
    assert dr.operation_phase_angle1 is None
    assert dr.operation_phase_angle2 is None
    assert dr.operation_phase_angle3 is None


@given(**distance_relay_kwargs)
def test_distance_relay_constructor_kwargs(backward_blind,
                                           backward_reach,
                                           backward_reactance,
                                           forward_blind,
                                           forward_reach,
                                           forward_reactance,
                                           operation_phase_angle1,
                                           operation_phase_angle2,
                                           operation_phase_angle3,
                                           **kwargs):
    dr = DistanceRelay(
        backward_blind=backward_blind,
        backward_reach=backward_reach,
        backward_reactance=backward_reactance,
        forward_blind=forward_blind,
        forward_reach=forward_reach,
        forward_reactance=forward_reactance,
        operation_phase_angle1=operation_phase_angle1,
        operation_phase_angle2=operation_phase_angle2,
        operation_phase_angle3=operation_phase_angle3,
        **kwargs
    )

    verify_protection_relay_function_constructor_kwargs(dr, **kwargs)
    assert dr.backward_blind == backward_blind
    assert dr.backward_reach == backward_reach
    assert dr.backward_reactance == backward_reactance
    assert dr.forward_blind == forward_blind
    assert dr.forward_reach == forward_reach
    assert dr.forward_reactance == forward_reactance
    assert dr.operation_phase_angle1 == operation_phase_angle1
    assert dr.operation_phase_angle2 == operation_phase_angle2
    assert dr.operation_phase_angle3 == operation_phase_angle3


def test_distance_relay_constructor_args():
    dr = DistanceRelay(*distance_relay_args)

    verify_protection_relay_function_constructor_args(dr)
    assert dr.backward_blind == distance_relay_args[-9]
    assert dr.backward_reach == distance_relay_args[-8]
    assert dr.backward_reactance == distance_relay_args[-7]
    assert dr.forward_blind == distance_relay_args[-6]
    assert dr.forward_reach == distance_relay_args[-5]
    assert dr.forward_reactance == distance_relay_args[-4]
    assert dr.operation_phase_angle1 == distance_relay_args[-3]
    assert dr.operation_phase_angle2 == distance_relay_args[-2]
    assert dr.operation_phase_angle3 == distance_relay_args[-1]
