#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import text, floats

from cim.iec61970.base.meas.test_measurement_value import measurement_value_kwargs, verify_measurement_value_constructor_default, \
    verify_measurement_value_constructor_kwargs, verify_measurement_value_constructor_args, measurement_value_args
from cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE, FLOAT_MIN, FLOAT_MAX
from zepben.evolve import AnalogValue

analog_value_kwargs = {
    **measurement_value_kwargs,
    "value": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "analog_mrid": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
}

analog_value_args = [*measurement_value_args, 1.1, "a"]


def test_analog_value_constructor_default():
    av = AnalogValue()

    verify_measurement_value_constructor_default(av)
    assert av.value == 0.0
    assert not av.analog_mrid


@given(**analog_value_kwargs)
def test_analog_value_constructor_kwargs(value, analog_mrid, **kwargs):
    # noinspection PyArgumentList
    av = AnalogValue(value=value,
                     analog_mrid=analog_mrid,
                     **kwargs)

    verify_measurement_value_constructor_kwargs(av, **kwargs)
    assert av.value == value
    assert av.analog_mrid == analog_mrid


def test_analog_value_constructor_args():
    # noinspection PyArgumentList
    av = AnalogValue(*analog_value_args)

    verify_measurement_value_constructor_args(av)
    assert av.value == analog_value_args[-2]
    assert av.analog_mrid == analog_value_args[-1]
