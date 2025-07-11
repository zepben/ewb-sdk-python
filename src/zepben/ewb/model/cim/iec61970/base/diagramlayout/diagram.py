#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Diagram"]

from typing import Optional, Dict, List, Generator, TYPE_CHECKING

from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.model.cim.iec61970.base.diagramlayout.diagram_style import DiagramStyle
from zepben.ewb.model.cim.iec61970.base.diagramlayout.orientation_kind import OrientationKind
from zepben.ewb.util import nlen, ngen, require, safe_remove_by_id

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.diagramlayout.diagram_object import DiagramObject


class Diagram(IdentifiedObject):
    """
    The diagram being exchanged. The coordinate system is a standard Cartesian coordinate system and the orientation
    attribute defines the orientation.
    """

    diagram_style: DiagramStyle = DiagramStyle.SCHEMATIC
    """A Diagram may have a DiagramStyle."""

    orientation_kind: OrientationKind = OrientationKind.POSITIVE
    """Coordinate system orientation of the diagram."""

    _diagram_objects: Optional[Dict[str, DiagramObject]] = None

    def __init__(self, diagram_objects: List[DiagramObject] = None, **kwargs):
        super(Diagram, self).__init__(**kwargs)
        if diagram_objects:
            for obj in diagram_objects:
                self.add_diagram_object(obj)

    def num_diagram_objects(self):
        """
        Returns The number of `DiagramObject`s associated with this `Diagram`
        """
        return nlen(self._diagram_objects)

    @property
    def diagram_objects(self) -> Generator[DiagramObject, None, None]:
        """
        The diagram objects belonging to this diagram.
        """
        return ngen(self._diagram_objects.values() if self._diagram_objects is not None else None)

    def get_diagram_object(self, mrid: str) -> DiagramObject:
        """
        Get the `DiagramObject` for this `Diagram` identified by `mrid`

        `mrid` the mRID of the required `DiagramObject`
        Returns The `DiagramObject` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        if not self._diagram_objects:
            raise KeyError(mrid)
        try:
            return self._diagram_objects[mrid]
        except AttributeError:
            raise KeyError(mrid)

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

        self._diagram_objects = dict() if self._diagram_objects is None else self._diagram_objects
        self._diagram_objects[diagram_object.mrid] = diagram_object

        return self

    def remove_diagram_object(self, diagram_object: DiagramObject) -> Diagram:
        """
        Disassociate `diagram_object` from this `Diagram`

        `diagram_object` the `DiagramObject` to disassociate with this `Diagram`.
        Returns A reference to this `Diagram` to allow fluent use.
        Raises `KeyError` if `diagram_object` was not associated with this `Diagram`.
        """
        self._diagram_objects = safe_remove_by_id(self._diagram_objects, diagram_object)
        return self

    def clear_diagram_objects(self) -> Diagram:
        """
        Clear all `DiagramObject`s.
        Returns A reference to this `Diagram` to allow fluent use.
        """
        self._diagram_objects = None
        return self
