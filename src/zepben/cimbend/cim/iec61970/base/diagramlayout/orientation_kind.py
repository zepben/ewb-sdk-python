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

from enum import Enum

__all__ = ["OrientationKind"]


class OrientationKind(Enum):
    """
    The orientation of the coordinate system with respect to top, left, and the coordinate number system.
    """

    # For 2D diagrams, a positive orientation will result in X values increasing from left to right and Y values
    # increasing from bottom to top.  This is also known as a right hand orientation.
    POSITIVE = 0

    # For 2D diagrams, a negative orientation gives the left-hand orientation (favoured by computer graphics displays)
    # with X values increasing from left to right and Y values increasing from top to bottom.   This is also known as
    # a left hand orientation.
    NEGATIVE = 1

    @property
    def short_name(self):
        return str(self)[16:]
