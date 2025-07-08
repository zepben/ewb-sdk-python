#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["DiagramObject"]

from typing import Optional, List, Generator, Callable, TYPE_CHECKING

from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.model.cim.iec61970.base.diagramlayout.diagram_object_point import DiagramObjectPoint
from zepben.ewb.util import nlen, ngen, require, safe_remove

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.diagramlayout.diagram import Diagram

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

    def for_each_point(self, action: Callable[[int, DiagramObjectPoint], None]):
        """
        Call the `action` on each :class:`DiagramObjectPoint` in the `points` collection

        :param action: An action to apply to each :class:`DiagramObjectPoint` in the `points` collection, taking the index of the point, and the point itself.
        """
        for index, point in enumerate(self.points):
            action(index, point)

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
                        f"adding the items in order and there are no gaps in the numbering.")
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

    def remove_point_by_sequence_number(self, sequence_number: int) -> DiagramObjectPoint:
        """
        Remove a :class:`DiagramObjectPoint` from this :class:`DiagramObject` by its sequence number.

        NOTE: This will update the sequence numbers of all items located after the removed sequence number.

        :param sequence_number: The sequence number of the `DiagramObjectPoint` to remove.
        :return: The :class:`DiagramObjectPoint` that was removed, or null if there was no :class:`DiagramObjectPoint` for the given `sequenceNumber`.
        :raises IndexError: If no :class:`DiagramObjectPoint` with the specified `sequence_number` was not associated with this :class:`DiagramObject`.
        """
        point = self.get_point(sequence_number)
        self._diagram_object_points = safe_remove(self._diagram_object_points, point)
        return point

    def clear_points(self) -> DiagramObject:
        """
        Clear all points.
        Returns A reference to this `DiagramObject` to allow fluent use.
        """
        self._diagram_object_points = None
        return self
