"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations

from dataclasses import dataclass, InitVar, field
from typing import List, Optional, Dict, Generator, Tuple

from zepben.cimbend.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.cimbend.cim.iec61970.base.diagramlayout.diagram_object_style import DiagramObjectStyle
from zepben.cimbend.cim.iec61970.base.diagramlayout.diagram_style import DiagramStyle
from zepben.cimbend.cim.iec61970.base.diagramlayout.orientation_kind import OrientationKind
from zepben.cimbend.util import nlen, require, contains_mrid, ngen

__all__ = ["DiagramObjectPoint", "Diagram", "DiagramObject"]


@dataclass
class DiagramObjectPoint(object):
    """
    A point in a given space defined by 3 coordinates and associated to a diagram object.  The coordinates may be positive
    or negative as the origin does not have to be in the corner of a diagram.

    Attributes -
    x_position : The X coordinate of this point.
    y_position : The Y coordinate of this point.
    """
    x_position: float = 0.0
    y_position: float = 0.0

    def __str__(self):
        return f"x:{self.x_position}|y:{self.y_position}"


@dataclass
class DiagramObject(IdentifiedObject):
    """
    An object that defines one or more points in a given space. This object can be associated with anything
    that specializes IdentifiedObject. For single line diagrams such objects typically include such items as
    analog values, breakers, disconnectors, power transformers, and transmission lines.

    Attributes -
        diagram : A diagram object is part of a diagram.
        identifiedObjectMRID : The domain object to which this diagram object is associated.
        style : A diagram object has a style associated that provides a reference for the style used in the originating system.
        rotation : Sets the angle of rotation of the diagram object.  Zero degrees is pointing to the top of the diagram.
                   Rotation is clockwise.
    """
    diagram: Optional[Diagram] = None
    identified_object_mrid: Optional[str] = None
    style: DiagramObjectStyle = DiagramObjectStyle.NONE
    rotation: float = 0.0
    diagramobjectpoints: InitVar[List[DiagramObjectPoint]] = field(default=list())
    _diagram_object_points: Optional[List[DiagramObjectPoint]] = field(init=False, default=None)

    def __post_init__(self, diagramobjectpoints: List[DiagramObjectPoint]):
        super().__post_init__()
        for point in diagramobjectpoints:
            self.add_point(point)

    @property
    def num_points(self):
        """
        :return: The number of :class:`DiagramObjectPoint`s associated with this ``DiagramObject``
        """
        return nlen(self._diagram_object_points)

    @property
    def points(self) -> Generator[Tuple[int, DiagramObjectPoint], None, None]:
        """
        :return: Generator over the ``DiagramObjectPoint``s of this ``DiagramObject``.
        """
        for i, point in enumerate(ngen(self._diagram_object_points)):
            yield i, point

    def get_point(self, sequence_number: int) -> DiagramObjectPoint:
        """
        Get the ``sequence_number`` ``DiagramObjectPoint`` for this ``DiagramObject``.

        :param sequence_number: The sequence number of the ``DiagramObjectPoint`` to get.
        :return: The :class:`DiagramObjectPoint` identified by ``sequence_number``
        :raises: IndexError if this ``DiagramObject`` didn't contain ``sequence_number`` points.
        """
        if self._diagram_object_points is not None:
            return self._diagram_object_points[sequence_number]
        else:
            raise IndexError(sequence_number)

    def __getitem__(self, item: int) -> DiagramObjectPoint:
        return self.get_point(item)

    def add_point(self, point: DiagramObjectPoint) -> DiagramObject:
        """
        Add a ``DiagramObjectPoint`` to this ``DiagramObject``, assigning it a sequence_number of ``num_points``.
        :param point: The :class:`DiagramObjectPoint` to associate with this ``DiagramObject``.
        :return: A reference to this ``DiagramObject`` to allow fluent use.
        """
        return self.insert_point(point)

    def insert_point(self, point: DiagramObjectPoint, sequence_number: int = None) -> DiagramObject:
        """
        Add a ``DiagramObjectPoint`` to this ``DiagramObject``
        :param point: The :class:`DiagramObjectPoint` to associate with this ``DiagramObject``.
        :param sequence_number: The sequence number of the ``DiagramObjectPoint``.
        :return: A reference to this ``DiagramObject`` to allow fluent use.
        """
        if sequence_number is None:
            sequence_number = self.num_points
        require(0 <= sequence_number <= self.num_points,
                lambda: f"Unable to add DiagramObjectPoint to {str(self)}. Sequence number {sequence_number}"
                        f" is invalid. Expected a value between 0 and {self.num_points}. Make sure you are "
                        f"adding the points in the correct order and there are no missing sequence numbers.")
        self._diagram_object_points = list() if self._diagram_object_points is None else self._diagram_object_points
        self._diagram_object_points.insert(sequence_number, point)
        return self

    def __setitem__(self, key, value):
        self.insert_point(value, key)

    def remove_point(self, point: DiagramObjectPoint) -> DiagramObject:
        """
        :param point: the :class:`DiagramObjectPoint` to disassociate from this ``DiagramObject``.
        :raises: KeyError if ``point`` was not associated with this ``DiagramObject``.
        :return: A reference to this ``DiagramObject`` to allow fluent use.
        """
        if self._diagram_object_points is not None:
            self._diagram_object_points.remove(point)
            if not self._diagram_object_points:
                self._diagram_object_points = None
        else:
            raise KeyError(point)

        return self

    def clear_points(self) -> DiagramObject:
        """
        Clear all points.
        :return: A reference to this ``DiagramObject`` to allow fluent use.
        """
        self._diagram_object_points = None
        return self


@dataclass
class Diagram(IdentifiedObject):
    """
    The diagram being exchanged. The coordinate system is a standard Cartesian coordinate system and the orientation
    attribute defines the orientation.

    Attributes -
        diagram_style : A Diagram may have a DiagramStyle.
        orientationKind : Coordinate system orientation of the diagram.
    """

    diagram_style: DiagramStyle = DiagramStyle.SCHEMATIC
    orientation_kind: OrientationKind = OrientationKind.POSITIVE
    diagramobjects: InitVar[List[DiagramObject]] = field(default=list())
    _diagram_objects: Optional[Dict[str, DiagramObject]] = field(init=False, default=None)

    def __post_init__(self, diagramobjects: List[DiagramObject]):
        super().__post_init__()
        for obj in diagramobjects:
            self.add_object(obj)

    @property
    def num_objects(self):
        """
        :return: The number of :class:`DiagramObject`s associated with this ``Diagram``
        """
        return nlen(self._diagram_objects)

    @property
    def diagram_objects(self) -> Generator[DiagramObject, None, None]:
        """
        :return: Generator over the ``DiagramObject``s of this ``Diagram``.
        """
        return ngen(self._diagram_objects)

    def get_object(self, mrid: str) -> DiagramObject:
        """
        Get the ``DiagramObject`` for this ``Diagram`` identified by ``mrid``

        :param mrid: the mRID of the required :class:`DiagramObject`
        :return: The :class:`DiagramObject` with the specified ``mrid`` if it exists
        :raises: KeyError if mrid wasn't present.
        """
        return self._diagram_objects[mrid]

    def add_object(self, diagram_object: DiagramObject) -> DiagramObject:
        """
        :param diagram_object: the :class:`DiagramObject` to associate with this ``Diagram``.
        :return: The previous ``DiagramObject`` stored by ``diagram_object``s mrid, otherwise ``diagram_object`` is returned
        if there was no previous value.
        """
        require(diagram_object.diagram is self, lambda: f"{str(diagram_object)} references another Diagram "
                                                        f"{str(diagram_object.diagram)}, expected {str(self)}.")
        require(not contains_mrid(self._diagram_objects, diagram_object.mrid),
                lambda: f"A DiagramObject with mRID ${diagram_object.mrid} already exists in {str(self)}.")
        self._diagram_objects = dict() if self._diagram_objects is None else self._diagram_objects
        return self._diagram_objects.setdefault(diagram_object.mrid, diagram_object)

    def remove_object(self, diagram_object: DiagramObject) -> DiagramObject:
        """
        :param diagram_object: the :class:`DiagramObject` to disassociate with this ``Diagram``.
        :raises: KeyError if ``diagram_object`` was not associated with this ``Diagram``.
        :return: The previous ``DiagramObject`` stored by ``diagram_object``s mrid if it existed.
        """
        if self._diagram_objects is not None:
            previous = self._diagram_objects[diagram_object.mrid]
            del self._diagram_objects[diagram_object.mrid]
        else:
            raise KeyError(diagram_object)

        if not self._diagram_objects:
            self._diagram_objects = None
        return previous

    def clear_objects(self) -> Diagram:
        """
        Clear all ``DiagramObject``s.
        :return: A reference to this ``Diagram`` to allow fluent use.
        """
        self._diagram_objects = None
        return self
