#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["DiagramObjectPoint"]

from dataclasses import dataclass


@dataclass(frozen=True)
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
