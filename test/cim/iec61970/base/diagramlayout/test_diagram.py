#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import lists, builds, sampled_from

from test.cim.extract_testing_args import extract_testing_args
from test.cim.collection_validator import validate_collection_unordered
from test.cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from zepben.evolve import DiagramObject, DiagramStyle, Diagram, OrientationKind
from zepben.evolve.model.cim.iec61970.base.diagramlayout.create_diagram_layout_components import create_diagram

diagram_kwargs = {
    **identified_object_kwargs,
    "diagram_style": sampled_from(DiagramStyle),
    "orientation_kind": sampled_from(OrientationKind),
    "diagram_objects": lists(builds(DiagramObject))
}

# noinspection PyArgumentList
diagram_args = [*identified_object_args, DiagramStyle.GEOGRAPHIC, OrientationKind.NEGATIVE, {"do": DiagramObject()}]


def test_diagram_constructor_default():
    d = Diagram()
    d2 = create_diagram()
    validate_default_diagram(d)
    validate_default_diagram(d2)


def validate_default_diagram(d):
    verify_identified_object_constructor_default(d)
    assert d.diagram_style == DiagramStyle.SCHEMATIC
    assert d.orientation_kind == OrientationKind.POSITIVE
    assert not list(d.diagram_objects)


@given(**diagram_kwargs)
def test_diagram_constructor_kwargs(diagram_style, orientation_kind, diagram_objects, **kwargs):
    args = extract_testing_args(locals())
    d = Diagram(**args, **kwargs)
    validate_diagram_values(d, **args, **kwargs)


@given(**diagram_kwargs)
def test_diagram_creator(diagram_style, orientation_kind, diagram_objects, **kwargs):
    args = extract_testing_args(locals())
    d = create_diagram(**args, **kwargs)
    validate_diagram_values(d, **args, **kwargs)


def validate_diagram_values(d, diagram_style, orientation_kind, diagram_objects, **kwargs):
    verify_identified_object_constructor_kwargs(d, **kwargs)
    assert d.diagram_style == diagram_style
    assert d.orientation_kind == orientation_kind
    assert list(d.diagram_objects) == diagram_objects


def test_diagram_constructor_args():
    d = Diagram(*diagram_args)

    verify_identified_object_constructor_args(d)
    assert d.diagram_style == diagram_args[-3]
    assert d.orientation_kind == diagram_args[-2]
    assert list(d.diagram_objects) == list(diagram_args[-1].values())


def test_diagram_objects_collection():
    validate_collection_unordered(Diagram,
                                  lambda mrid, d: DiagramObject(mrid, diagram=d),
                                  Diagram.num_diagram_objects,
                                  Diagram.get_diagram_object,
                                  Diagram.diagram_objects,
                                  Diagram.add_diagram_object,
                                  Diagram.remove_diagram_object,
                                  Diagram.clear_diagram_objects,
                                  KeyError)


def test_auto_two_way_connections_for_diagram_constructor():
    do = DiagramObject()
    d = create_diagram(diagram_objects=[do])

    assert do.diagram == d
