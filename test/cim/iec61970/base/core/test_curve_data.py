#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import floats, one_of, none
from pytest import raises
from zepben.evolve import CurveData

from cim.cim_creators import FLOAT_MIN, FLOAT_MAX

curve_data_kwargs = {
    "x_value": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "y1_value": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "y2_value": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
    "y3_value": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX))
}

curve_data_args = [1.1, 2.2, 3.3, 4.4]


# noinspection PyArgumentList
def test_curve_data_constructor_default():
    #
    # NOTE: There is no blank constructor, so check we need to pass both required values.
    #
    with raises(TypeError):
        CurveData()
    with raises(TypeError):
        CurveData(1.0)
    with raises(TypeError):
        CurveData(x_value=2.0)
    with raises(TypeError):
        CurveData(y1_value=2.0)

    # Make sure we can call the constructor without the optional args.
    CurveData(x_value=1.0, y1_value=2.0)
    CurveData(x_value=1.0, y1_value=2.0, y2_value=3.0)
    CurveData(x_value=1.0, y1_value=2.0, y3_value=4.0)
    CurveData(x_value=1.0, y1_value=2.0, y2_value=3.0, y3_value=4.0)


@given(**curve_data_kwargs)
def test_curve_data_constructor_kwargs(x_value, y1_value, y2_value, y3_value, **kwargs):
    assert not kwargs

    curve_data = CurveData(x_value=x_value, y1_value=y1_value, y2_value=y2_value, y3_value=y3_value)

    assert curve_data.x_value == x_value
    assert curve_data.y1_value == y1_value
    assert curve_data.y2_value == y2_value
    assert curve_data.y3_value == y3_value


def test_curve_data_constructor_args():
    curve_data = CurveData(*curve_data_args)

    assert curve_data_args[-4:] == [
        curve_data.x_value,
        curve_data.y1_value,
        curve_data.y2_value,
        curve_data.y3_value
    ]
