#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Diagram"]

from typing import Optional, Dict, List, Generator, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.model.cim.iec61970.base.diagramlayout.diagram_style import DiagramStyle
from zepben.ewb.model.cim.iec61970.base.diagramlayout.orientation_kind import OrientationKind
from zepben.ewb.util import nlen, ngen, require, safe_remove_by_id

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.diagramlayout.diagram_object import DiagramObject


@dataslot
@boilermaker
class Diagram(IdentifiedObject):
    """
    The diagram being exchanged. The coordinate system is a standard Cartesian coordinate system and the orientation
    attribute defines the orientation.
    """

    diagram_style: DiagramStyle = DiagramStyle.SCHEMATIC
    """A Diagram may have a DiagramStyle."""

    orientation_kind: OrientationKind = OrientationKind.POSITIVE
    """Coordinate system orientation of the diagram."""

    diagram_objects: List[DiagramObject] | None = MRIDDictAccessor()

    def _retype(self):
        self.diagram_objects: MRIDDictRouter[DiagramObject] = ...
    
    @deprecated("BOILERPLATE: Use len(diagram_objects) instead")
    def num_diagram_objects(self):
        return len(self.diagram_objects)

    @deprecated("BOILERPLATE: Use diagram_objects.get_by_mrid(mrid) instead")
    def get_diagram_object(self, mrid: str) -> DiagramObject:
        """
        Get the `DiagramObject` for this `Diagram` identified by `mrid`

        `mrid` the mRID of the required `DiagramObject`
        Returns The `DiagramObject` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return self.diagram_objects.get_by_mrid(mrid)

    @custom_add(diagram_objects)
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

        if self._validate_reference(diagram_object, self.get_diagram_object, "A DiagramObject"):
            return self

        self.diagram_objects.append_unchecked(diagram_object)

        return self

    @deprecated("Boilerplate: Use diagram_objects.remove(diagram_object) instead")
    def remove_diagram_object(self, diagram_object: DiagramObject) -> Diagram:
        self.diagram_objects.remove(diagram_object)
        return self

    @deprecated("BOILERPLATE: Use diagram_objects.clear() instead")
    def clear_diagram_objects(self) -> Diagram:
        self.diagram_objects.clear()
        return self

