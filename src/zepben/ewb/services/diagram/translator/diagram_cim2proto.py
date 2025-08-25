#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["diagram_to_pb", "diagram_object_to_pb", "diagram_object_point_to_pb"]

from zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramObjectPoint_pb2 import DiagramObjectPoint as PBDiagramObjectPoint
from zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramObject_pb2 import DiagramObject as PBDiagramObject
from zepben.protobuf.cim.iec61970.base.diagramlayout.Diagram_pb2 import Diagram as PBDiagram

from zepben.ewb.model.cim.iec61970.base.diagramlayout.diagram import Diagram
from zepben.ewb.model.cim.iec61970.base.diagramlayout.diagram_object import DiagramObject
from zepben.ewb.model.cim.iec61970.base.diagramlayout.diagram_object_point import DiagramObjectPoint
from zepben.ewb.services.common.translator.base_cim2proto import identified_object_to_pb, set_or_null, bind_to_pb
from zepben.ewb.services.common.translator.util import mrid_or_empty
# noinspection PyProtectedMember
from zepben.ewb.services.diagram.translator.diagram_enum_mappers import _map_diagram_style, _map_orientation_kind


################################
# IEC61970 Base Diagram Layout #
################################

@bind_to_pb
def diagram_to_pb(cim: Diagram) -> PBDiagram:
    return PBDiagram(
        io=identified_object_to_pb(cim),
        diagramStyle=_map_diagram_style.to_pb(cim.diagram_style),
        orientationKind=_map_orientation_kind.to_pb(cim.orientation_kind),
        diagramObjectMRIDs=[str(io.mrid) for io in cim.diagram_objects]
    )


@bind_to_pb
def diagram_object_to_pb(cim: DiagramObject) -> PBDiagramObject:
    return PBDiagramObject(
        io=identified_object_to_pb(cim),
        diagramMRID=mrid_or_empty(cim.diagram),
        identifiedObjectMRID=cim.identified_object_mrid,
        diagramObjectPoints=[diagram_object_point_to_pb(io) for io in cim.points],
        rotation=cim.rotation,
        **set_or_null(
            diagramObjectStyle=cim.style,
        )
    )


@bind_to_pb
def diagram_object_point_to_pb(cim: DiagramObjectPoint) -> PBDiagramObjectPoint:
    return PBDiagramObjectPoint(xPosition=cim.x_position, yPosition=cim.y_position)
