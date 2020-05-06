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


from dataclasses import dataclass

from zepben.cimbend.common.base_proto2cim import *
from zepben.cimbend.diagram.diagrams import DiagramService
from zepben.protobuf.cim.iec61970.base.diagramlayout.Diagram_pb2 import Diagram as PBDiagram
from zepben.protobuf.cim.iec61970.base.diagramlayout.OrientationKind_pb2 import OrientationKind as PBOrientationKind
from zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramStyle_pb2 import DiagramStyle as PBDiagramStyle
from zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramObject_pb2 import DiagramObject as PBDiagramObject
from zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramObjectPoint_pb2 import \
    DiagramObjectPoint as PBDiagramObjectPoint
from zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramObjectStyle_pb2 import \
    DiagramObjectStyle as PBDiagramObjectStyle

from zepben.cimbend.cim.iec61970.base.diagramlayout import Diagram, DiagramObject, DiagramObjectPoint
from zepben.cimbend.cim.iec61970.base.diagramlayout.diagram_object_style import DiagramObjectStyle
from zepben.cimbend.cim.iec61970.base.diagramlayout.diagram_style import DiagramStyle
from zepben.cimbend.cim.iec61970.base.diagramlayout.orientation_kind import OrientationKind

__all__ = ["diagramobjectpoint_from_pb", "DiagramProtoToCim"]


def diagramobjectpoint_from_pb(pb: PBDiagramObjectPoint) -> DiagramObjectPoint:
    return DiagramObjectPoint(pb.xPosition, pb.yPosition)


@dataclass
class DiagramProtoToCim(BaseProtoToCim):
    service: DiagramService

    # IEC61970 DIAGRAM LAYOUT #
    def add_diagram(self, pb: PBDiagram):
        cim = Diagram(pb.mrid())
        set_identifiedobject(pb.io, cim)
        cim.orientation_kind = OrientationKind[PBOrientationKind.Name(pb.orientationKind)]
        cim.diagram_style = DiagramStyle[PBDiagramStyle.Name(pb.diagramStyle)]
        self.service.add(cim)

    def add_diagramobject(self, pb: PBDiagramObject):
        diagram = self._get(pb.diagramMRID, Diagram, pb.name_and_mrid())
        cim = DiagramObject(diagram, pb.mrid())
        set_identifiedobject(pb.io, cim)
        cim.identified_object_mrid = pb.identifiedObjectMRID
        cim.style = DiagramObjectStyle[PBDiagramObjectStyle.Name(pb.diagramObjectStyle)]
        for point in pb.diagramObjectPoints:
            cim.add_point(diagramobjectpoint_from_pb(point))
        self.service.add_diagram_object(cim)
