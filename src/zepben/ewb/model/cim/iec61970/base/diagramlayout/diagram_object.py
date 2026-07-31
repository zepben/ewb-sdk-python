#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["DiagramObject"]

from dataclasses import field
from typing import Optional, List, Callable, TYPE_CHECKING, Any

from typing_extensions import deprecated

from zepben.ewb import Alias
from zepben.ewb.boilerplate.collections.lazy_list import LazyList
from zepben.ewb.boilerplate.backfill import internal
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.model.cim.iec61970.base.diagramlayout.diagram_object_point import DiagramObjectPoint
from zepben.ewb.boilerplate.dataclass_base import zb_dataclass

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.diagramlayout.diagram import Diagram

@zb_dataclass
class DiagramObject(IdentifiedObject):
    """
    An object that defines one or more points in a given space. This object can be associated with anything
    that specializes IdentifiedObject. For single line diagrams such objects typically include such items as
    analog values, breakers, disconnectors, power transformers, and transmission lines.
    """

    _diagram: Optional[Diagram] = field(default=None)

    identified_object_mrid: Optional[str] = None
    """The domain object to which this diagram object is associated."""

    style: Optional[str] = None
    """A diagram object has a style associated that provides a reference for the style used in the originating system."""

    rotation: float = 0.0
    """Sets the angle of rotation of the diagram object.  Zero degrees is pointing to the top of the diagram. Rotation is clockwise."""

    _diagram_object_points: Optional[List[DiagramObjectPoint]] = field(default=None)

    def __init__(self, *args, diagram_object_points=None, **kwargs):
        super(DiagramObject, self).__init__(*args, **kwargs)
        self.points.extend(diagram_object_points)

    @property
    @internal(_diagram)
    def diagram(self):
        """A diagram object is part of a diagram."""
        return self._diagram

    @diagram.setter
    @deprecated("diagram should never be set directly - it is automatically set when adding it to the `diagram_objects` list")
    def diagram(self, diag):
        if self._diagram is None or self._diagram is diag:
            self._diagram = diag
        else:
            raise ValueError(f"diagram for {str(self)} has already been set to {self._diagram}, cannot reset this field to {diag}")

    points: LazyList[DiagramObjectPoint] = LazyList(
        _diagram_object_points,
        "DiagramObjectPoint",
    )

    # region deprecated list boilerplate
    #
    # ("region/endregion" is an IntelliJ feature letting you hide the entire thing)
    # This boilerplate exists solely to enable backwards compatibility.
    # It will be removed eventually.
    # Every single method simply forwards the call to the corresponding list.

    # region points boilerplate

    @deprecated("Use points.for_each_indexed(action) instead.")
    def for_each_point(
        self,
        action: Callable[[int, DiagramObjectPoint], Any],
    ):
        self.points.for_each_indexed(action)

    @deprecated("Use len(points) instead.")
    def num_points(self):
        return len(self.points)

    @deprecated("Use points[sequence_number] instead.")
    def get_point(self, sequence_number: int) -> DiagramObjectPoint:
        return self.points[sequence_number]

    @deprecated("Use points[item] instead.")
    def __getitem__(self, item: int) -> DiagramObjectPoint:
        return self.points[item]

    @deprecated("Use points.append(point) instead.")
    def add_point(self, point: DiagramObjectPoint) -> DiagramObject:
        self.points.append(point)
        return self

    @deprecated("Use points.insert(sequence_number, point)")
    def insert_point(
        self,
        point: DiagramObjectPoint,
        sequence_number: int | None = None,
    ) -> DiagramObject:
        if sequence_number is None: sequence_number = len(self.points)
        self.points.insert(sequence_number, point)

        return self

    @deprecated("Use points.insert(key, value) instead.")
    def __setitem__(
        self,
        key: int,
        value: DiagramObjectPoint,
    ) -> None:
        self.points.insert(key, value)

    @deprecated("Use points.remove(point) instead.")
    def remove_point(self, point: DiagramObjectPoint) -> DiagramObject:
        self.points.remove(point)
        return self

    @deprecated("Use points.pop(sequence_number) instead.")
    def remove_point_by_sequence_number(
        self,
        sequence_number: int,
    ) -> DiagramObjectPoint:
        return self.points.pop(sequence_number)

    @deprecated("Use points.clear() instead.")
    def clear_points(self) -> DiagramObject:
        self.points.clear()
        return self

    # endregion

    # endregion

