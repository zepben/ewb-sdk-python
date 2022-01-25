#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import List, Optional, Generator

from dataclassy import dataclass

from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.evolve.util import require, nlen, ngen, safe_remove

__all__ = ["PositionPoint", "Location", "StreetAddress", "TownDetail", "StreetDetail"]


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

    @property
    def latitude(self):
        return self.y_position


@dataclass(slots=True)
class TownDetail(object):
    """
    Town details, in the context of address.
    """

    name: Optional[str] = None
    """Town name."""
    state_or_province: Optional[str] = None
    """Name of the state or province."""

    def all_fields_null_or_empty(self):
        """Check to see if all fields of this `TownDetail` are null or empty."""
        return not (self.name or self.state_or_province)


@dataclass(slots=True)
class StreetDetail(object):
    """
    Street details, in the context of address.
    """

    building_name: str = ""
    """
    (if applicable) In certain cases the physical location of the place of interest does not have a direct point of entry from the street, 
    but may be located inside a larger structure such as a building, complex, office block, apartment, etc.
    """
    floor_identification: str = ""
    """The identification by name or number, expressed as text, of the floor in the building as part of this address."""
    name: str = ""
    """Name of the street."""
    number: str = ""
    """Designator of the specific location on the street."""
    suite_number: str = ""
    """Number of the apartment or suite."""
    type: str = ""
    """Type of street. Examples include: street, circle, boulevard, avenue, road, drive, etc."""
    display_address: str = ""
    """The address as it should be displayed to a user."""

    def all_fields_empty(self):
        """Check to see if all fields of this `StreetDetail` are empty."""
        return not (
            self.building_name or
            self.floor_identification or
            self.name or
            self.number or
            self.suite_number or
            self.type or
            self.display_address
        )


@dataclass(slots=True)
class StreetAddress(object):
    """
    General purpose street and postal address information.
    """

    postal_code: str = ""
    """Postal code for the address."""
    town_detail: Optional[TownDetail] = None
    """Optional `TownDetail` for this address."""
    po_box: str = ""
    """Post office box for the address."""
    street_detail: Optional[StreetDetail] = None
    """Optional `StreetDetail` for this address."""


class Location(IdentifiedObject):
    """
    The place, scene, or point of something where someone or something has been, is, and/or will be at a given moment in time.
    It can be defined with one or more `PositionPoint`'s.
    """
    main_address: Optional[StreetAddress] = None
    """Main address of the location."""

    _position_points: Optional[List[PositionPoint]] = None

    def __init__(self, position_points: List[PositionPoint] = None, **kwargs):
        """
        `position_points` A list of `PositionPoint`s to associate with this `Location`.
        """
        super(Location, self).__init__(**kwargs)
        if position_points:
            for point in position_points:
                self.add_point(point)

    def num_points(self):
        """
        Returns The number of `PositionPoint`s in this `Location`
        """
        return nlen(self._position_points)

    @property
    def points(self) -> Generator[PositionPoint, None, None]:
        """
        Returns Generator over the `PositionPoint`s of this `Location`.
        """
        for point in ngen(self._position_points):
            yield point

    def get_point(self, sequence_number: int) -> Optional[PositionPoint]:
        """
        Get the `sequence_number` `PositionPoint` for this `Location`.

        `sequence_number` The sequence number of the `PositionPoint` to get.
        Returns The `PositionPoint` identified by `sequence_number`
        Raises IndexError if this `Location` didn't contain `sequence_number` points.
        """
        return self._position_points[sequence_number] if 0 <= sequence_number < nlen(self._position_points) else None

    def __getitem__(self, item):
        return self.get_point(item)

    def add_point(self, point: PositionPoint) -> Location:
        """
        Associate a `PositionPoint` with this `Location`, assigning it a sequence_number of `num_points`.
        `point` The `PositionPoint` to associate with this `Location`.
        Returns A reference to this `Location` to allow fluent use.
        """
        return self.insert_point(point)

    def insert_point(self, point: PositionPoint, sequence_number: int = None) -> Location:
        """
        Associate a `PositionPoint` with this `Location`

        `point` The `PositionPoint` to associate with this `Location`.
        `sequence_number` The sequence number of the `PositionPoint`.
        Returns A reference to this `Location` to allow fluent use.
        Raises `ValueError` if `sequence_number` < 0 or > `num_points()`.
        """
        if sequence_number is None:
            sequence_number = self.num_points()
        require(0 <= sequence_number <= self.num_points(),
                lambda: f"Unable to add PositionPoint to {str(self)}. Sequence number {sequence_number} "
                        f"is invalid. Expected a value between 0 and {self.num_points()}. Make sure you are "
                        f"adding the points in the correct order and there are no gaps in the numbering.")
        self._position_points = list() if self._position_points is None else self._position_points
        self._position_points.insert(sequence_number, point)
        return self

    def __setitem__(self, key, value):
        return self.insert_point(value, key)

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
