#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve import *

__all__ = ["create_diagram", "create_diagram_object", "create_diagram_object_point"]


def create_diagram(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, diagram_style: DiagramStyle = DiagramStyle.SCHEMATIC,
                   orientation_kind: OrientationKind = OrientationKind.POSITIVE, diagram_objects: List[DiagramObject] = None) -> Diagram:
    """
    Diagram(IdentifiedObject)
    IdentifiedObject: mrid, name, description, names
    Diagram: diagram_style, orientation_kind, diagram_objects
    """
    d = Diagram(**locals())
    if diagram_objects:
        for obj in diagram_objects:
            obj.diagram = d
    return d


def create_diagram_object(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, diagram: Diagram = None,
                          identified_object_mrid: str = None, style: str = None, rotation: float = 0.0, diagram_object_points: List[DiagramObjectPoint] = None
                          ) -> DiagramObject:
    """
    DiagramObject(IdentifiedObject)
    IdentifiedObject: mrid, name, description, names
    DiagramObject: diagram, identified_object_mrid, style, rotation, diagram_object_points
    """
    do = DiagramObject(**locals())
    if diagram:
        diagram.add_diagram_object(do)
    return do


def create_diagram_object_point(x_position: float, y_position: float) -> DiagramObjectPoint:
    """
    DiagramObjectPoint()
    DiagramObjectPoint: x_position, y_position
    """
    # noinspection PyArgumentList
    return DiagramObjectPoint(**locals())

