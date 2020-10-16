#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from dataclassy import dataclass
from typing import List, Optional, Generator, Tuple

from zepben.cimbend.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.cimbend.util import require, nlen, ngen, safe_remove

__all__ = ["PositionPoint", "Location", "StreetAddress", "TownDetail"]


@dataclass(slots=True, frozen=True)
class PositionPoint(object):
    """
    Set of spatial coordinates that determine a point, defined in WGS84 (latitudes and longitudes).

    Use a single position point instance to desribe a point-oriented location.
    Use a sequence of position points to describe a line-oriented object (physical location of non-point oriented
    objects like cables or lines), or area of an object (like a substation or a geographical zone - in this case,
    have first and last position point with the same values).
    """

    x_position: float
    """X axis position - longitude"""
    y_position: float
    """Y axis position - latitude"""

    def __init__(self):
        require(-90.0 <= self.y_position <= 90.0,
                lambda: f"Latitude is out of range. Expected -90 to 90, got {self.y_position}.")
        require(-180.0 <= self.x_position <= 180.0,
                lambda: f"Longitude is out of range. Expected -180 to 180, got {self.x_position}.")

    def __str__(self):
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


@dataclass(slots=True)
class TownDetail(object):
    """
    Town details, in the context of address.
    """

    name: str = ""
    """Town name."""
    state_or_province: str = ""
    """Name of the state or province."""


@dataclass(slots=True)
class StreetAddress(object):
    """
    General purpose street and postal address information.
    """

    postal_code: str = ""
    """Postal code for the address."""
    town_detail: Optional[TownDetail] = None
    """Optional `TownDetail` for this address."""


class Location(IdentifiedObject):
    """
    The place, scene, or point of something where someone or something has been, is, and/or will be at a given moment in time.
    It can be defined with one or more `PositionPoint`'s.
    """
    main_address: Optional[StreetAddress] = None
    """Main address of the location."""

    _position_points: Optional[List[PositionPoint]] = None

    def __init__(self, position_points: List[PositionPoint] = None):
        """
        `position_points` A list of `PositionPoint`s to associate with this `Location`.
        """
        if position_points:
            for point in position_points:
                self.add_point(point)

    def num_points(self):
        """
        Returns The number of `PositionPoint`s in this `Location`
        """
        return nlen(self._position_points)

    @property
    def points(self) -> Generator[Tuple[int, PositionPoint], None, None]:
        """
        Returns Generator over the `PositionPoint`s of this `Location`.
        """
        for i, point in enumerate(ngen(self._position_points)):
            yield i, point

    def get_point(self, sequence_number: int) -> Optional[PositionPoint]:
        """
        Get the `sequence_number` `PositionPoint` for this `DiagramObject`.

        `sequence_number` The sequence number of the `PositionPoint` to get.
        Returns The `PositionPoint` identified by `sequence_number`
        Raises IndexError if this `Location` didn't contain `sequence_number` points.
        """
        return self._position_points[sequence_number] if 0 < nlen(self._position_points) < sequence_number else None

    def __getitem__(self, item):
        return self.get_point(item)

    def add_point(self, point: PositionPoint, sequence_number: int = None) -> Location:
        """
        Associate a `PositionPoint` with this `Location`
        `point` The `PositionPoint` to associate with this `Location`.
        `sequence_number` The sequence number of the `PositionPoint`.
        Returns A reference to this `Location` to allow fluent use.
        Raises `ValueError` if `sequence_number` is set and not between 0 and `num_points()`
        """
        if sequence_number is None:
            sequence_number = self.num_points()
        require(0 <= sequence_number <= self.num_points(),
                lambda: f"Unable to add PositionPoint to Location {str(self)}. Sequence number {sequence_number} is invalid. "
                        f"Expected a value between 0 and {self.num_points()}. Make sure you are adding the points in order and there are no gaps in the numbering.")
        self._position_points = [] if self._position_points is None else self._position_points
        self._position_points.insert(sequence_number, point)
        return self

    def __setitem__(self, key, value):
        return self.add_point(value, key)

    def remove_point(self, point: PositionPoint) -> Location:
        """
        Remove a `PositionPoint` from this `Location`
        `point` The `PositionPoint` to remove.
        Raises `ValueError` if `point` was not part of this `Location`
        Returns A reference to this `Location` to allow fluent use.
        """
        self._position_points = safe_remove(self._position_points, point)
        return self

    def clear_points(self) -> Location:
        self._position_points = None
        return self
