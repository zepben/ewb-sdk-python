#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import zepben.cimbend.common.resolver as resolver

from zepben.cimbend.common.translator.base_proto2cim import *
from zepben.cimbend.diagram.diagrams import DiagramService
from zepben.protobuf.cim.iec61970.base.diagramlayout.Diagram_pb2 import Diagram as PBDiagram
from zepben.protobuf.cim.iec61970.base.diagramlayout.OrientationKind_pb2 import OrientationKind as PBOrientationKind
from zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramStyle_pb2 import DiagramStyle as PBDiagramStyle
from zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramObject_pb2 import DiagramObject as PBDiagramObject
from zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramObjectPoint_pb2 import DiagramObjectPoint as PBDiagramObjectPoint
from zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramObjectStyle_pb2 import DiagramObjectStyle as PBDiagramObjectStyle

from zepben.cimbend.cim.iec61970.base.diagramlayout import Diagram, DiagramObject, DiagramObjectPoint
from zepben.cimbend.cim.iec61970.base.diagramlayout.diagram_object_style import DiagramObjectStyle
from zepben.cimbend.cim.iec61970.base.diagramlayout.diagram_style import DiagramStyle
from zepben.cimbend.cim.iec61970.base.diagramlayout.orientation_kind import OrientationKind

__all__ = ["diagramobjectpoint_to_cim", "diagram_to_cim", "diagramobject_to_cim"]


def diagramobjectpoint_to_cim(pb: PBDiagramObjectPoint) -> DiagramObjectPoint:
    return DiagramObjectPoint(pb.xPosition, pb.yPosition)


# IEC61970 DIAGRAM LAYOUT #
def diagram_to_cim(pb: PBDiagram, service: DiagramService):
    cim = Diagram(mrid=pb.mrid(),
                  orientation_kind=OrientationKind[PBOrientationKind.Name(pb.orientationKind)],
                  diagram_style=DiagramStyle[PBDiagramStyle.Name(pb.diagramStyle)])
    for mrid in pb.diagramObjectMRIDs:
        service.resolve_or_defer_reference(resolver.diagram_objects(cim), mrid)
    identifiedobject_to_cim(pb.io, cim, service)
    service.add(cim)


def diagramobject_to_cim(pb: PBDiagramObject, service: DiagramService):
    cim = DiagramObject(mrid=pb.mrid(), identified_object_mrid=pb.identifiedObjectMRID,
                        style=DiagramObjectStyle[PBDiagramObjectStyle.Name(pb.diagramObjectStyle)])
    service.resolve_or_defer_reference(resolver.diagram(cim), pb.diagramMRID)
    for point in pb.diagramObjectPoints:
        cim.add_point(diagramobjectpoint_to_cim(point))
    identifiedobject_to_cim(pb.io, cim, service)
    service.add_diagram_object(cim)


PBDiagram.to_cim = diagram_to_cim
PBDiagramObject.to_cim = diagramobject_to_cim
PBDiagramObjectPoint.to_cim = diagramobjectpoint_to_cim
