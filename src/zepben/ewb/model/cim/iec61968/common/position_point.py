#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["PositionPoint"]

from dataclasses import dataclass

from zepben.ewb.util import require


@dataclass(frozen=True)
class PositionPoint(object):
    """
    Set of spatial coordinates that determine a point, defined in WGS84 (latitudes and longitudes).

    Use a single position point instance to describe a point-oriented location.
    Use a sequence of position points to describe a line-oriented object (physical location of non-point oriented
    objects like cables or lines), or area of an object (like a substation or a geographical zone - in this case,
    have first and last position point with the same values).
    """

    x_position: float
    """X axis position - longitude"""
    y_position: float
    """Y axis position - latitude"""

    def __post_init__(self):
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
