#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import lists, builds, text, floats, data

from test.cim.common_testing_functions import verify
from test.cim.collection_verifier import verify_collection_ordered
from test.cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from test.cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE, create_diagram_object_point
from zepben.evolve import DiagramObject, DiagramObjectPoint, Diagram
from zepben.evolve.model.cim.iec61970.base.diagramlayout.create_diagram_layout_components import create_diagram_object

diagram_object_kwargs = {
    **identified_object_kwargs,
    "diagram": builds(Diagram),
    "identified_object_mrid": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "style": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "rotation": floats(min_value=0, max_value=360),
    "diagram_object_points": lists(create_diagram_object_point(), max_size=2)
}

# noinspection PyArgumentList
diagram_object_args = [*identified_object_args, Diagram(), "a", "CB", 1.1, [DiagramObjectPoint(1.1, 2.2)]]


def test_diagram_object_constructor_default():
    do = DiagramObject()
    do2 = create_diagram_object()
    verify_default_diagram_object(do)
    verify_default_diagram_object(do2)


def verify_default_diagram_object(do):
    verify_identified_object_constructor_default(do)
    assert not do.diagram
    assert not do.identified_object_mrid
    assert not do.style
    assert do.rotation == 0.0
    assert not list(do.points)


# noinspection PyShadowingNames
@given(data())
def test_diagram_object_constructor_kwargs(data):
    verify(
        [DiagramObject, create_diagram_object],
        data, diagram_object_kwargs, verify_diagram_object_values
    )


def verify_diagram_object_values(do, diagram, identified_object_mrid, style, rotation, diagram_object_points, **kwargs):
    verify_identified_object_constructor_kwargs(do, **kwargs)
    assert do.diagram == diagram
    assert do.identified_object_mrid == identified_object_mrid
    assert do.style == style
    assert do.rotation == rotation
    assert list(do.points) == diagram_object_points


def test_diagram_object_constructor_args():
    do = DiagramObject(*diagram_object_args)

    verify_identified_object_constructor_args(do)
    assert do.diagram == diagram_object_args[-5]
    assert do.identified_object_mrid == diagram_object_args[-4]
    assert do.style == diagram_object_args[-3]
    assert do.rotation == diagram_object_args[-2]
    assert list(do.points) == diagram_object_args[-1]


def test_points_collection():
    # noinspection PyArgumentList
    verify_collection_ordered(DiagramObject,
                              lambda i, _: DiagramObjectPoint(i, i),
                              DiagramObject.num_points,
                              DiagramObject.get_point,
                              DiagramObject.points,
                              DiagramObject.add_point,
                              DiagramObject.insert_point,
                              DiagramObject.remove_point,
                              DiagramObject.clear_points)


def test_auto_two_way_connections_for_diagram_object_constructor():
    d = Diagram()
    do = create_diagram_object(diagram=d)

    assert d.get_diagram_object(do.mrid) == do