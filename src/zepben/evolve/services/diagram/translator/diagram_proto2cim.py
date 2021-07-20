#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramObjectPoint_pb2 import DiagramObjectPoint as PBDiagramObjectPoint
from zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramObject_pb2 import DiagramObject as PBDiagramObject
from zepben.protobuf.cim.iec61970.base.diagramlayout.Diagram_pb2 import Diagram as PBDiagram

import zepben.evolve.services.common.resolver as resolver
from zepben.evolve import identified_object_to_cim, OrientationKind, DiagramStyle
from zepben.evolve.model.cim.iec61970.base.diagramlayout.diagram_layout import Diagram, DiagramObject, DiagramObjectPoint
from zepben.evolve.services.diagram.diagrams import DiagramService

__all__ = ["diagram_object_point_to_cim", "diagram_to_cim", "diagram_object_to_cim"]


################################
# IEC61970 BASE DIAGRAM LAYOUT #
################################

def diagram_to_cim(pb: PBDiagram, service: DiagramService):
    cim = Diagram(
        mrid=pb.mrid(),
        orientation_kind=OrientationKind(pb.orientationKind),
        diagram_style=DiagramStyle(pb.diagramStyle)
    )

    for mrid in pb.diagramObjectMRIDs:
        service.resolve_or_defer_reference(resolver.diagram_objects(cim), mrid)

    identified_object_to_cim(pb.io, cim, service)
    return cim if service.add(cim) else None


def diagram_object_to_cim(pb: PBDiagramObject, service: DiagramService):
    cim = DiagramObject(
        mrid=pb.mrid(),
        identified_object_mrid=pb.identifiedObjectMRID if pb.identifiedObjectMRID else None,
        style=pb.diagramObjectStyle if pb.diagramObjectStyle else None,
        rotation=pb.rotation,
    )

    service.resolve_or_defer_reference(resolver.diagram(cim), pb.diagramMRID)
    for point in pb.diagramObjectPoints:
        cim.add_point(diagram_object_point_to_cim(point))

    identified_object_to_cim(pb.io, cim, service)
    return cim if service.add_diagram_object(cim) else None


def diagram_object_point_to_cim(pb: PBDiagramObjectPoint) -> DiagramObjectPoint:
    # noinspection PyArgumentList
    return DiagramObjectPoint(pb.xPosition, pb.yPosition)


PBDiagram.to_cim = diagram_to_cim
PBDiagramObject.to_cim = diagram_object_to_cim
PBDiagramObjectPoint.to_cim = diagram_object_point_to_cim
