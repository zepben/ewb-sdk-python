#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import integers, text

from cim.iec61970.base.meas.test_measurement_value import measurement_value_kwargs, verify_measurement_value_constructor_default, \
    verify_measurement_value_constructor_kwargs, verify_measurement_value_constructor_args, measurement_value_args
from cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER, ALPHANUM, TEXT_MAX_SIZE
from zepben.evolve import DiscreteValue

discrete_value_kwargs = {
    **measurement_value_kwargs,
    "value": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "discrete_mrid": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
}

discrete_value_args = [*measurement_value_args, 1, "a"]


def test_discrete_value_constructor_default():
    dv = DiscreteValue()

    verify_measurement_value_constructor_default(dv)
    assert dv.value == 0
    assert not dv.discrete_mrid


@given(**discrete_value_kwargs)
def test_discrete_value_constructor_kwargs(value, discrete_mrid, **kwargs):
    # noinspection PyArgumentList
    dv = DiscreteValue(value=value,
                       discrete_mrid=discrete_mrid,
                       **kwargs)

    verify_measurement_value_constructor_kwargs(dv, **kwargs)
    assert dv.value == value
    assert dv.discrete_mrid == discrete_mrid


def test_discrete_value_constructor_args():
    # noinspection PyArgumentList
    dv = DiscreteValue(*discrete_value_args)

    verify_measurement_value_constructor_args(dv)
    assert dv.value == discrete_value_args[-2]
    assert dv.discrete_mrid == discrete_value_args[-1]
