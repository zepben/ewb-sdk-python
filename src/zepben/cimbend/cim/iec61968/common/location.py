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

from dataclasses import dataclass
from typing import List, Optional, Generator, Tuple

from zepben.cimbend.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.cimbend.util import require, nlen, ngen

__all__ = ["PositionPoint", "Location", "StreetAddress", "TownDetail"]


@dataclass
class PositionPoint(object):
    """
    Set of spatial coordinates that determine a point, defined in WGS84 (latitudes and longitudes).

    Use a single position point instance to desribe a point-oriented location.
    Use a sequence of position points to describe a line-oriented object (physical location of non-point oriented
    objects like cables or lines), or area of an object (like a substation or a geographical zone - in this case,
    have first and last position point with the same values).

    Attributes:
        x_position : X axis position - longitude
        y_position : Y axis position - latitude
    """
    x_position: float = 0.0
    y_position: float = 0.0

    def __post_init__(self):
        require(-90.0 <= self.y_position <= 90,
                lambda: f"Latitude is out of range. Expected -90 to 90, got {self.y_position}.")
        require(-180.0 <= self.x_position <= 180,
                lambda: f"Longitude is out of range. Expected -180 to 180, got {self.x_position}.")

    def __str__(self):
        return f"{self.x_position}:{self.y_position}"

    def __repr__(self):
        return f"{self.x_position}:{self.y_position}"

    @property
    def longitude(self):
        return self.x_position

    @longitude.setter
    def longitude(self, lon):
        self.x_position = lon

    @property
    def latitude(self):
        return self.y_position

    @latitude.setter
    def latitude(self, lat):
        self.y_position = lat


@dataclass
class TownDetail(object):
    """
    Town details, in the context of address.

    Attributes -
        name : Town name.
        stateOrProvince : Name of the state or province.
    """

    name: str = ""
    state_or_province: str = ""


@dataclass
class StreetAddress(object):
    """
    General purpose street and postal address information.

    Attributes -
        postal_code : Postal code for the address.
        town_detail : TownDetail
    """

    postal_code: str = ""
    town_detail: Optional[TownDetail] = None


@dataclass
class Location(IdentifiedObject):
    """
    The place, scene, or point of something where someone or something has been, is, and/or will be at a given moment
    in time. It can be defined with one or more :class:`PositionPoint`'s.

    Attributes:
        main_address : Main address of the location.
        _position_points : List of :class:`PositionPoint`. The ordering of the list is important, and refers to the
                          `sequenceNumber` of each PositionPoint.

    """
    main_address: Optional[StreetAddress] = None
    _position_points: Optional[List[PositionPoint]] = None

    @property
    def num_points(self):
        """
        :return: The number of :class:`PositionPoint`s in this ``Location``
        """
        return nlen(self._position_points)

    @property
    def points(self) -> Generator[Tuple[int, PositionPoint], None, None]:
        """
        :return: Generator over the ``PositionPoint``s of this ``Location``.
        """
        for i, point in enumerate(ngen(self._position_points)):
            yield i, point

    def get_point(self, sequence_number: int) -> Optional[PositionPoint]:
        """
        Get the ``sequence_number`` ``PositionPoint`` for this ``DiagramObject``.

        :param sequence_number: The sequence number of the ``PositionPoint`` to get.
        :return: The :class:`PositionPoint` identified by ``sequence_number``
        :raises: IndexError if this ``Location`` didn't contain ``sequence_number`` points.
        """
        return self._position_points[sequence_number] if 0 < nlen(self._position_points) < sequence_number else None

    def __getitem__(self, item):
        return self.get_point(item)

    def add_point(self, point: PositionPoint, sequence_number: int = None) -> Location:
        """
        Add a :class:`PositionPoint` to this ``Location``
        :param point: The :class:`PositionPoint` to associate with this ``Location``.
        :param sequence_number: The sequence number of the ``PositionPoint``.
        :return: A reference to this ``Location`` to allow fluent use.
        """
        if sequence_number is None:
            sequence_number = self.num_points
        require(0 <= sequence_number <= self.num_points,
                lambda: f"Unable to add PositionPoint to Location {str(self)}. Sequence number {sequence_number} is invalid. "
                        f"Expected a value between 0 and {self.num_points}. Make sure you are adding the points in the correct order and there are no missing sequence numbers.")
        self._position_points = [] if self._position_points is None else self._position_points
        self._position_points.insert(sequence_number, point)
        return self

    def __setitem__(self, key, value):
        return self.add_point(value, key)

    def remove_point(self, point: PositionPoint) -> Location:
        """
        Remove a ``PositionPoint`` from this ``Location``
        :param point:
        :raises: ValueError if ``point`` was not part of this ``Location``
        :return: True if the point was removed, False otherwise.
        """
        if self._position_points is not None:
            self._position_points.remove(point)
            if not self._position_points:
                self._position_points = None
        else:
            raise KeyError(point)

        return self

    def clear_points(self) -> Location:
        self._position_points = None
        return self
