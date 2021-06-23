#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import List, Optional, Dict, Generator

from dataclassy import dataclass

from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.evolve.model.cim.iec61970.base.diagramlayout.diagram_style import DiagramStyle
from zepben.evolve.model.cim.iec61970.base.diagramlayout.orientation_kind import OrientationKind
from zepben.evolve.util import nlen, require, ngen, safe_remove, safe_remove_by_id

__all__ = ["DiagramObjectPoint", "Diagram", "DiagramObject"]


@dataclass(slots=True)
class DiagramObjectPoint(object):
    """
    A point in a given space defined by 3 coordinates and associated to a diagram object.  The coordinates may be positive
    or negative as the origin does not have to be in the corner of a diagram.
    """

    x_position: float
    """The X coordinate of this point."""

    y_position: float
    """The Y coordinate of this point."""

    def __str__(self):
        return f"x:{self.x_position}|y:{self.y_position}"


class DiagramObject(IdentifiedObject):
    """
    An object that defines one or more points in a given space. This object can be associated with anything
    that specializes IdentifiedObject. For single line diagrams such objects typically include such items as
    analog values, breakers, disconnectors, power transformers, and transmission lines.
    """

    _diagram: Optional[Diagram] = None
    """A diagram object is part of a diagram."""

    identified_object_mrid: Optional[str] = None
    """The domain object to which this diagram object is associated."""

    style: Optional[str] = None
    """A diagram object has a style associated that provides a reference for the style used in the originating system."""

    rotation: float = 0.0
    """Sets the angle of rotation of the diagram object.  Zero degrees is pointing to the top of the diagram. Rotation is clockwise."""

    _diagram_object_points: Optional[List[DiagramObjectPoint]] = None

    def __init__(self, diagram: Diagram = None, diagram_object_points: List[DiagramObjectPoint] = None, **kwargs):
        super(DiagramObject, self).__init__(**kwargs)
        if diagram:
            self.diagram = diagram
        if diagram_object_points:
            for point in diagram_object_points:
                self.add_point(point)

    @property
    def diagram(self):
        return self._diagram

    @diagram.setter
    def diagram(self, diag):
        if self._diagram is None or self._diagram is diag:
            self._diagram = diag
        else:
            raise ValueError(f"diagram for {str(self)} has already been set to {self._diagram}, cannot reset this field to {diag}")

    def num_points(self):
        """
        Returns the number of `DiagramObjectPoint`s associated with this `DiagramObject`
        """
        return nlen(self._diagram_object_points)

    @property
    def points(self) -> Generator[DiagramObjectPoint, None, None]:
        """
        The `DiagramObjectPoint`s for this `DiagramObject`.
        """
        return ngen(self._diagram_object_points)

    def get_point(self, sequence_number: int) -> DiagramObjectPoint:
        """
        Get the `DiagramObjectPoint` for this `DiagramObject` represented by `sequence_number` .
        A diagram object can have 0 or more points to reflect its layout position, routing (for polylines) or boundary (for polygons).
        Index in the underlying points collection corresponds to the sequence number

        `sequence_number` The sequence number of the `DiagramObjectPoint` to get.
        Returns The `DiagramObjectPoint` identified by `sequence_number`
        Raises IndexError if this `DiagramObject` didn't contain `sequence_number` points.
        """
        if self._diagram_object_points is not None:
            return self._diagram_object_points[sequence_number]
        else:
            raise IndexError(sequence_number)

    def __getitem__(self, item: int) -> DiagramObjectPoint:
        return self.get_point(item)

    def add_point(self, point: DiagramObjectPoint) -> DiagramObject:
        """
        Associate a `DiagramObjectPoint` with this `DiagramObject`, assigning it a sequence_number of `num_points`.
        `point` The `DiagramObjectPoint` to associate with this `DiagramObject`.
        Returns A reference to this `DiagramObject` to allow fluent use.
        """
        return self.insert_point(point)

    def insert_point(self, point: DiagramObjectPoint, sequence_number: int = None) -> DiagramObject:
        """
        Associate a `DiagramObjectPoint` with this `DiagramObject`

        `point` The `DiagramObjectPoint` to associate with this `DiagramObject`.
        `sequence_number` The sequence number of the `DiagramObjectPoint`.
        Returns A reference to this `DiagramObject` to allow fluent use.
        Raises `ValueError` if `sequence_number` < 0 or > `num_points()`.
        """
        if sequence_number is None:
            sequence_number = self.num_points()
        require(0 <= sequence_number <= self.num_points(),
                lambda: f"Unable to add DiagramObjectPoint to {str(self)}. Sequence number {sequence_number}"
                        f" is invalid. Expected a value between 0 and {self.num_points()}. Make sure you are "
                        f"adding the points in the correct order and there are no gaps in the numbering.")
        self._diagram_object_points = list() if self._diagram_object_points is None else self._diagram_object_points
        self._diagram_object_points.insert(sequence_number, point)
        return self

    def __setitem__(self, key, value):
        self.insert_point(value, key)

    def remove_point(self, point: DiagramObjectPoint) -> DiagramObject:
        """
        Disassociate `point` from this `DiagramObject`

        `point` The `DiagramObjectPoint` to disassociate from this `DiagramObject`.
        Returns A reference to this `DiagramObject` to allow fluent use.
        Raises `ValueError` if `point` was not associated with this `DiagramObject`.
        """
        self._diagram_object_points = safe_remove(self._diagram_object_points, point)
        return self

    def clear_points(self) -> DiagramObject:
        """
        Clear all points.
        Returns A reference to this `DiagramObject` to allow fluent use.
        """
        self._diagram_object_points = None
        return self


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
