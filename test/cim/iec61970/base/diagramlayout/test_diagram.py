#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import lists, builds, sampled_from

from cim.collection_validator import validate_collection_unordered
from cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from zepben.evolve import DiagramObject, DiagramStyle, Diagram, OrientationKind

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

    verify_identified_object_constructor_default(d)
    assert d.diagram_style == DiagramStyle.SCHEMATIC
    assert d.orientation_kind == OrientationKind.POSITIVE
    assert not list(d.diagram_objects)


@given(**diagram_kwargs)
def test_diagram_constructor_kwargs(diagram_style, orientation_kind, diagram_objects, **kwargs):
    d = Diagram(diagram_style=diagram_style,
                orientation_kind=orientation_kind,
                diagram_objects=diagram_objects,
                **kwargs)

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
