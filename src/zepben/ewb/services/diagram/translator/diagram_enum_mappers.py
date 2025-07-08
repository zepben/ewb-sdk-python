#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = []

from zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramStyle_pb2 import DiagramStyle as PBDiagramStyle
from zepben.protobuf.cim.iec61970.base.diagramlayout.OrientationKind_pb2 import OrientationKind as PBOrientationKind

from zepben.ewb.model.cim.iec61970.base.diagramlayout.diagram_style import DiagramStyle
from zepben.ewb.model.cim.iec61970.base.diagramlayout.orientation_kind import OrientationKind
# noinspection PyProtectedMember
from zepben.ewb.services.common.enum_mapper import EnumMapper

#
# NOTE: These are deliberately excluded from the module export, as they aren't part of the public api.
#

_map_diagram_style = EnumMapper(DiagramStyle, PBDiagramStyle)
_map_orientation_kind = EnumMapper(OrientationKind, PBOrientationKind)
