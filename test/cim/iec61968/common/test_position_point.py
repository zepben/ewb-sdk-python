#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from _pytest.python_api import raises
from hypothesis import given
from hypothesis.strategies import floats

from test.cim import extract_testing_args
from zepben.evolve import PositionPoint
from zepben.evolve.model.cim.iec61968.common.create_common_components import create_position_point

position_point_kwargs = {
    "x_position": floats(min_value=-180, max_value=180),
    "y_position": floats(min_value=-90, max_value=90)
}

position_point_args = [1.1, 2.2]


# noinspection PyArgumentList
def test_position_point_constructor_default():
    #
    # NOTE: There is no blank constructor, so check we need to pass both values.
    #
    with raises(TypeError):
        PositionPoint()
        create_position_point()
    with raises(TypeError):
        PositionPoint(1.0)
        create_position_point(1.0)
    with raises(TypeError):
        PositionPoint(x_position=2.0)
        create_position_point(x_position=2.0)
    with raises(TypeError):
        PositionPoint(y_position=2.0)
        create_position_point(y_position=2.0)


# noinspection PyArgumentList
@given(**position_point_kwargs)
def test_position_point_constructor_kwargs(x_position, y_position, **kwargs):
    args = extract_testing_args(locals())
    assert not kwargs

    pp = PositionPoint(**args)
    validate_position_point_values(pp, **args)


@given(**position_point_kwargs)
def test_position_point_creator(x_position, y_position, **kwargs):
    args = extract_testing_args(locals())
    assert not kwargs

    pp = create_position_point(**args)
    validate_position_point_values(pp, **args)


def validate_position_point_values(pp, x_position, y_position):
    assert pp.x_position == x_position
    assert pp.y_position == y_position


def test_position_point_constructor_args():
    # noinspection PyArgumentList
    pp = PositionPoint(*position_point_args)

    assert pp.x_position == position_point_args[-2]
    assert pp.y_position == position_point_args[-1]


# noinspection PyArgumentList
def test_position_point_constructor_validates():
    with raises(ValueError, match="Longitude is out of range. Expected -180 to 180, got -181.0."):
        PositionPoint(-181.0, 0)
    with raises(ValueError, match="Longitude is out of range. Expected -180 to 180, got 181.0."):
        PositionPoint(181.0, 0)
    with raises(ValueError, match="Latitude is out of range. Expected -90 to 90, got -91.0."):
        PositionPoint(0, -91.0)
    with raises(ValueError, match="Latitude is out of range. Expected -90 to 90, got 91.0."):
        PositionPoint(0, 91.0)
