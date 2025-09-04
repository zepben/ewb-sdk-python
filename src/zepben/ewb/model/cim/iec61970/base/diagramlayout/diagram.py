#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Diagram"]

from typing import Optional, Dict, List, TYPE_CHECKING

from zepben.ewb.collections.autoslot import autoslot_dataclass
from zepben.ewb.collections.mrid_dict import MRIDDict
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.model.cim.iec61970.base.diagramlayout.diagram_style import DiagramStyle
from zepben.ewb.model.cim.iec61970.base.diagramlayout.orientation_kind import OrientationKind
from zepben.ewb.util import require

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.diagramlayout.diagram_object import DiagramObject


@autoslot_dataclass
class Diagram(IdentifiedObject):
    """
    The diagram being exchanged. The coordinate system is a standard Cartesian coordinate system and the orientation
    attribute defines the orientation.
    """

    diagram_style: DiagramStyle = DiagramStyle.SCHEMATIC
    """A Diagram may have a DiagramStyle."""

    orientation_kind: OrientationKind = OrientationKind.POSITIVE
    """Coordinate system orientation of the diagram."""

    diagram_objects: Optional[Dict[str, DiagramObject]] = None

    def __post_init__(self):
        self.diagram_objects: MRIDDict[DiagramObject] = MRIDDict(self.diagram_objects)

    def __init__(self, diagram_objects: List[DiagramObject] = None, **kwargs):
        super(Diagram, self).__init__(**kwargs)
        if diagram_objects:
            for obj in diagram_objects:
                self.add_diagram_object(obj)

    def num_diagram_objects(self):
        """
        Returns The number of `DiagramObject`s associated with this `Diagram`
        """
        return len(self.diagram_objects)

    def get_diagram_object(self, mrid: str) -> DiagramObject:
        """
        Get the `DiagramObject` for this `Diagram` identified by `mrid`

        `mrid` the mRID of the required `DiagramObject`
        Returns The `DiagramObject` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return self.diagram_objects.get_by_mrid(mrid)

    def add_diagram_object(self, diagram_object: DiagramObject) -> Diagram:
        """
        Associate a `DiagramObject` with this `Diagram`.

        `diagram_object` the `DiagramObject` to associate with this `Diagram`.
        Returns The previous `DiagramObject` stored by `diagram_object`s mrid, otherwise `diagram_object` is returned
        if there was no previous value.
        Raises `ValueError` if another `DiagramObject` with the same `mrid` already exists for this `Diagram`, or if `diagram_object.diagram` is not this
        `Diagram`.
        """

        if not diagram_object.diagram:
            diagram_object.diagram = self
        require(diagram_object.diagram is self, lambda: f"{str(diagram_object)} references another Diagram "
                                                        f"{str(diagram_object.diagram)}, expected {str(self)}.")

        self.diagram_objects.add(diagram_object)

        return self

    def remove_diagram_object(self, diagram_object: DiagramObject) -> Diagram:
        """
        Disassociate `diagram_object` from this `Diagram`

        `diagram_object` the `DiagramObject` to disassociate with this `Diagram`.
        Returns A reference to this `Diagram` to allow fluent use.
        Raises `KeyError` if `diagram_object` was not associated with this `Diagram`.
        """
        self.diagram_objects.remove(diagram_object)
        return self

    def clear_diagram_objects(self) -> Diagram:
        """
        Clear all `DiagramObject`s.
        Returns A reference to this `Diagram` to allow fluent use.
        """
        self.diagram_objects.clear()
        return self
