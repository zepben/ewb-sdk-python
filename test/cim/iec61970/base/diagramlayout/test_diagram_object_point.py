#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import floats
from pytest import raises
from zepben.ewb.model.cim.iec61970.base.diagramlayout.diagram_object_point import DiagramObjectPoint

from cim.cim_creators import FLOAT_MIN, FLOAT_MAX

diagram_object_point_kwargs = {
    "x_position": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "y_position": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
}

diagram_object_point_args = [1.1, 2.2]


# noinspection PyArgumentList
def test_diagram_object_point_constructor_default():
    #
    # NOTE: There is no blank constructor, so check we need to pass both values.
    #
    with raises(TypeError):
        DiagramObjectPoint()
    with raises(TypeError):
        DiagramObjectPoint(1.0)
    with raises(TypeError):
        DiagramObjectPoint(x_position=2.0)
    with raises(TypeError):
        DiagramObjectPoint(y_position=2.0)


@given(**diagram_object_point_kwargs)
def test_diagram_object_point_constructor_kwargs(x_position, y_position, **kwargs):
    assert not kwargs

    dop = DiagramObjectPoint(x_position=x_position, y_position=y_position)

    assert dop.x_position == x_position
    assert dop.y_position == y_position


from pytest import mark
@mark.skip(reason="Args are deprecated")
def test_diagram_object_point_constructor_args():
    dop = DiagramObjectPoint(*diagram_object_point_args)

    assert diagram_object_point_args[-2:] == [
        dop.x_position,
        dop.y_position
    ]
