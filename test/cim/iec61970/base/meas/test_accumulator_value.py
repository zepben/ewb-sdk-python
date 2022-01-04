#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import integers, text, data

from test.cim.common_testing_functions import verify
from test.cim.iec61970.base.meas.test_measurement_value import measurement_value_kwargs, verify_measurement_value_constructor_default, \
    verify_measurement_value_constructor_kwargs, verify_measurement_value_constructor_args, measurement_value_args
from test.cim.cim_creators import MAX_32_BIT_INTEGER, ALPHANUM, TEXT_MAX_SIZE
from zepben.evolve import AccumulatorValue
from zepben.evolve.model.cim.iec61970.base.meas.create_meas_components import create_accumulator_value

accumulator_value_kwargs = {
    **measurement_value_kwargs,
    "value": integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
    "accumulator_mrid": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
}

accumulator_value_args = [*measurement_value_args, 1, "a"]


def test_accumulator_value_constructor_default():
    av = AccumulatorValue()
    av2 = create_accumulator_value()
    verify_default_accumulator_value(av)
    verify_default_accumulator_value(av2)


def verify_default_accumulator_value(av):
    verify_measurement_value_constructor_default(av)
    assert av.value == 0
    assert not av.accumulator_mrid


# noinspection PyShadowingNames
@given(data())
def test_accumulator_value_constructor_kwargs(data):
    verify(
        [AccumulatorValue, create_accumulator_value],
        data, accumulator_value_kwargs, verify_accumulator_value_values
    )


def verify_accumulator_value_values(av, value, accumulator_mrid, **kwargs):
    verify_measurement_value_constructor_kwargs(av, **kwargs)
    assert av.value == value
    assert av.accumulator_mrid == accumulator_mrid


def test_accumulator_value_constructor_args():
    # noinspection PyArgumentList
    av = AccumulatorValue(*accumulator_value_args)

    verify_measurement_value_constructor_args(av)
    assert av.value == accumulator_value_args[-2]
    assert av.accumulator_mrid == accumulator_value_args[-1]
