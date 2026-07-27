#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Diagram"]

from dataclasses import field
from typing import Dict

from typing_extensions import deprecated

from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb.boilerplate.collections.mrid_list import MridCollection, Backfill
from zepben.ewb.boilerplate.collections.mrid_map import LazyMridMap
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.model.cim.iec61970.base.diagramlayout.diagram_object import DiagramObject
from zepben.ewb.model.cim.iec61970.base.diagramlayout.diagram_style import DiagramStyle
from zepben.ewb.model.cim.iec61970.base.diagramlayout.orientation_kind import OrientationKind


@zb_dataclass
class Diagram(IdentifiedObject):
    """
    The diagram being exchanged. The coordinate system is a standard Cartesian coordinate system and the orientation
    attribute defines the orientation.
    """

    diagram_style: DiagramStyle = DiagramStyle.SCHEMATIC
    """A Diagram may have a DiagramStyle."""

    orientation_kind: OrientationKind = OrientationKind.POSITIVE
    """Coordinate system orientation of the diagram."""

    _diagram_objects: Dict[str, DiagramObject] | None = field(default=None)

    diagram_objects: MridCollection[DiagramObject] = LazyMridMap(
        _diagram_objects,
        "A DiagramObject",
        backfill=Backfill(DiagramObject.diagram)
    )
    """The diagram objects belonging to this diagram."""


    # region deprecated list boilerplate
    # region cuts boilerplate

    @deprecated("Use len(diagram_objects) instead")
    def num_diagram_objects(self):
        return len(self.diagram_objects)

    @deprecated("Use diagram_objects.get_by_mrid(mrid) instead")
    def get_diagram_object(self, mrid: str) -> DiagramObject:
        return self.diagram_objects.get_by_mrid(mrid)

    @deprecated("Use diagram_objects.append(diagram_object) instead")
    def add_diagram_object(self, diagram_object: DiagramObject) -> Diagram:
        self.diagram_objects.append(diagram_object)
        return self

    @deprecated("Use diagram_objects.remove(diagram_object) instead")
    def remove_diagram_object(self, diagram_object: DiagramObject) -> Diagram:
        self.diagram_objects.remove(diagram_object)
        return self

    @deprecated("Use diagram_objects.clear() instead")
    def clear_diagram_objects(self) -> Diagram:
        self.diagram_objects.clear()
        return self

    # endregion
    # endregion