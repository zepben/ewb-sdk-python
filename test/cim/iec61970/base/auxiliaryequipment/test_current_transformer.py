#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import integers

from cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER
from cim.iec61970.base.auxiliaryequipment.test_sensor import sensor_kwargs, verify_sensor_constructor_default, \
    verify_sensor_constructor_kwargs, verify_sensor_constructor_args, sensor_args
from cim.property_validator import validate_property_accessor
from zepben.evolve import CurrentTransformer, CurrentTransformerInfo

current_transformer_kwargs = {
    **sensor_kwargs,
    "core_burden": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)
}
current_transformer_args = [*sensor_args, 1]


def test_current_transformer_constructor_default():
    ct = CurrentTransformer()

    verify_sensor_constructor_default(ct)
    assert ct.core_burden is None


@given(**current_transformer_kwargs)
def test_current_transformer_constructor_kwargs(core_burden, **kwargs):
    # noinspection PyArgumentList
    ct = CurrentTransformer(core_burden=core_burden, **kwargs)

    verify_sensor_constructor_kwargs(ct, **kwargs)
    assert ct.core_burden == core_burden


def test_current_transformer_constructor_args():
    # noinspection PyArgumentList
    ct = CurrentTransformer(*current_transformer_args)

    verify_sensor_constructor_args(ct)
    assert ct.core_burden == current_transformer_args[-1]


def test_current_transformer_info_accessor():
    validate_property_accessor(CurrentTransformer, CurrentTransformerInfo, CurrentTransformer.current_transformer_info)
