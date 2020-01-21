"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""


from zepben.cim.iec61970 import DiagramObjectPoint as PBDiagramObjectPoint, DiagramObject as PBDiagramObject, DiagramStyle, OrientationKind, DiagramObjectStyle
from zepben.model.identified_object import IdentifiedObject
from typing import List


class DiagramObjectPoint(object):
    def __init__(self, x, y):
        self.x_position = x
        self.y_position = y

    def __str__(self):
        return f"xPos: {self.x_position}, yPos: {self.y_position}"

    def __repr__(self):
        return f"xPos: {self.x_position}, yPos: {self.y_position}"

    def to_pb(self):
        return PBDiagramObjectPoint(xPosition=self.x_position, yPosition=self.y_position)

    @staticmethod
    def from_pb(pb_dop, **kwargs):
        return DiagramObjectPoint(pb_dop.xPosition, pb_dop.yPosition)


class DiagramObject(IdentifiedObject):
    def __init__(self, mrid: str, points: List[DiagramObjectPoint] = None, name: str = "", diagram=None,
                 object_style: DiagramObjectStyle = DiagramObjectStyle.NONE, rotation: float = 0.0):
        self._diagram = diagram
        self.diagram_object_points = points if points is not None else []
        self.diagram_object_style = object_style
        self.rotation = rotation
        super().__init__(mrid, name)

    @property
    def diagram(self):
        return self._diagram

    @diagram.setter
    def diagram(self, diagram):
        self._diagram = diagram

    def add_point(self, diag_obj_point):
        self.diagram_object_points.append(diag_obj_point)

    def to_pb(self):
        args = self._pb_args()
        if self.diagram:
            args["diagramMRID"] = self.diagram.mrid
        # TODO: Support diagramObjects on a DiagramObject?
        del args["diagramObjects"]
        return PBDiagramObject(**args)

    @staticmethod
    def from_pb(pb_do, **kwargs):
        """
        Transform a protobuf DiagramObject to a cimbend DiagramObject
        :param pb_do:
        :return:
        """
        diagram = Diagram(pb_do.diagramMRID)
        cim_diag_obj = DiagramObject(mrid=pb_do.mRID, name=pb_do.name, object_style=pb_do.diagramObjectStyle,
                                     rotation=pb_do.rotation, diagram=diagram)
        for point in pb_do.diagramObjectPoints:
            cim_diag_obj.add_point(DiagramObjectPoint.from_pb(point))
        return cim_diag_obj


class Diagram(IdentifiedObject):
    def __init__(self, mrid: str = "", name: str = "", diagram_style: DiagramStyle = DiagramStyle.SCHEMATIC,
                 orientation: OrientationKind = OrientationKind.POSITIVE):
        self.diagram_style = diagram_style
        self.orientation_kind = orientation
        self.objects = []  # Diagram objects belonging to this diagram
        super().__init__(mrid, name)

    def add_diagram_object(self, diagram_object: DiagramObject):
        """
        TODO:
        :return:
        """
        self.objects.append(diagram_object)

    def from_pb(pb_d, **kwargs):
        raise NotImplementedError()

    def to_pb(self):
        raise NotImplementedError()
