#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["diagram_object_point_to_cim", "diagram_to_cim", "diagram_object_to_cim"]

from zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramObjectPoint_pb2 import DiagramObjectPoint as PBDiagramObjectPoint
from zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramObject_pb2 import DiagramObject as PBDiagramObject
from zepben.protobuf.cim.iec61970.base.diagramlayout.Diagram_pb2 import Diagram as PBDiagram

import zepben.ewb.services.common.resolver as resolver
from zepben.ewb import identified_object_to_cim, OrientationKind, DiagramStyle, add_to_network_or_none, bind_to_cim
from zepben.ewb.model.cim.iec61970.base.diagramlayout.diagram import Diagram
from zepben.ewb.model.cim.iec61970.base.diagramlayout.diagram_object import DiagramObject
from zepben.ewb.model.cim.iec61970.base.diagramlayout.diagram_object_point import DiagramObjectPoint
from zepben.ewb.services.common.translator.base_proto2cim import get_nullable
from zepben.ewb.services.diagram.diagrams import DiagramService


################################
# IEC61970 Base Diagram Layout #
################################

@bind_to_cim
@add_to_network_or_none
def diagram_to_cim(pb: PBDiagram, service: DiagramService):
    cim = Diagram(
        mrid=pb.mrid(),
        orientation_kind=OrientationKind(pb.orientationKind),
        diagram_style=DiagramStyle(pb.diagramStyle)
    )

    for mrid in pb.diagramObjectMRIDs:
        service.resolve_or_defer_reference(resolver.diagram_objects(cim), mrid)

    identified_object_to_cim(pb.io, cim, service)
    return cim


@bind_to_cim
def diagram_object_to_cim(pb: PBDiagramObject, service: DiagramService):
    cim = DiagramObject(
        mrid=pb.mrid(),
        identified_object_mrid=pb.identifiedObjectMRID if pb.identifiedObjectMRID else None,
        style=get_nullable(pb, 'diagramObjectStyle'),
        rotation=pb.rotation,
    )

    service.resolve_or_defer_reference(resolver.diagram(cim), pb.diagramMRID)
    for point in pb.diagramObjectPoints:
        cim.add_point(diagram_object_point_to_cim(point))

    identified_object_to_cim(pb.io, cim, service)
    return cim if service.add_diagram_object(cim) else None


@bind_to_cim
def diagram_object_point_to_cim(pb: PBDiagramObjectPoint) -> DiagramObjectPoint:
    # noinspection PyArgumentList
    return DiagramObjectPoint(pb.xPosition, pb.yPosition)
