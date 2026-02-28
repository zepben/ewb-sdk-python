#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import sampled_from, booleans

from cim.iec61970.base.protection.test_protection_relay_function import protection_relay_function_kwargs, protection_relay_function_args, \
    verify_protection_relay_function_constructor_default, verify_protection_relay_function_constructor_args, verify_protection_relay_function_constructor_kwargs
from streaming.get.pb_creators import floats, FLOAT_MIN, FLOAT_MAX
from zepben.ewb import PolarizingQuantityType, PhaseCode, generate_id, DirectionalCurrentRelay


directional_current_relay_kwargs = {
    **protection_relay_function_kwargs,
    'directional_characteristic_angle': floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    'polarizing_quantity_type': sampled_from(PolarizingQuantityType),
    'relay_element_phase': sampled_from(PhaseCode),
    'minimum_pickup_current': floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    'current_limit_1': floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    'inverse_time_flag': booleans(),
    'time_delay_1': floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
}


directional_current_relay_args = [
    *protection_relay_function_args,
    1.1,
    PolarizingQuantityType.NEGATIVE_SEQUENCE_VOLTAGE,
    PhaseCode.ABCN,
    2.2,
    3.3,
    False,
    4.4,
]


def test_directional_current_relay_constructor_default():
    dcr = DirectionalCurrentRelay(mrid=generate_id())

    verify_protection_relay_function_constructor_default(dcr)
    assert dcr.directional_characteristic_angle is None
    assert dcr.polarizing_quantity_type == PolarizingQuantityType.UNKNOWN
    assert dcr.relay_element_phase == PhaseCode.NONE
    assert dcr.minimum_pickup_current is None
    assert dcr.current_limit_1 is None
    assert dcr.inverse_time_flag is None
    assert dcr.time_delay_1 is None


@given(**directional_current_relay_kwargs)
def test_directional_current_relay_constructor_kwargs(
    directional_characteristic_angle,
    polarizing_quantity_type,
    relay_element_phase,
    minimum_pickup_current,
    current_limit_1,
    inverse_time_flag,
    time_delay_1,
    **kwargs
):
    dcr = DirectionalCurrentRelay(
        directional_characteristic_angle=directional_characteristic_angle,
        polarizing_quantity_type=polarizing_quantity_type,
        relay_element_phase=relay_element_phase,
        minimum_pickup_current=minimum_pickup_current,
        current_limit_1=current_limit_1,
        inverse_time_flag=inverse_time_flag,
        time_delay_1=time_delay_1,
        **kwargs
    )

    verify_protection_relay_function_constructor_kwargs(dcr, **kwargs)
    assert dcr.directional_characteristic_angle == directional_characteristic_angle
    assert dcr.polarizing_quantity_type == polarizing_quantity_type
    assert dcr.relay_element_phase == relay_element_phase
    assert dcr.minimum_pickup_current == minimum_pickup_current
    assert dcr.current_limit_1 == current_limit_1
    assert dcr.inverse_time_flag == inverse_time_flag
    assert dcr.time_delay_1 == time_delay_1


def test_directional_current_relay_constructor_args():
    dcr = DirectionalCurrentRelay(*directional_current_relay_args)

    verify_protection_relay_function_constructor_args(dcr)
    assert dcr.directional_characteristic_angle == directional_current_relay_args[-7]
    assert dcr.polarizing_quantity_type == directional_current_relay_args[-6]
    assert dcr.relay_element_phase == directional_current_relay_args[-5]
    assert dcr.minimum_pickup_current == directional_current_relay_args[-4]
    assert dcr.current_limit_1 == directional_current_relay_args[-3]
    assert dcr.inverse_time_flag == directional_current_relay_args[-2]
    assert dcr.time_delay_1 == directional_current_relay_args[-1]
