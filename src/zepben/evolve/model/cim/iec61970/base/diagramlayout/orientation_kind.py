#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum

__all__ = ["OrientationKind"]


class OrientationKind(Enum):
    """
    The orientation of the coordinate system with respect to top, left, and the coordinate number system.
    """

    POSITIVE = 0
    """For 2D diagrams, a positive orientation will result in X values increasing from left to right and Y values increasing from bottom to top.  
    This is also known as a right hand orientation."""

    NEGATIVE = 1
    """For 2D diagrams, a negative orientation gives the left-hand orientation (favoured by computer graphics displays) with X values increasing from left to 
    right and Y values increasing from top to bottom. This is also known as a left hand orientation."""

    @property
    def short_name(self):
        return str(self)[16:]
