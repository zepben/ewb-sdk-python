


#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum

__all__ = ["Direction"]


class Direction(Enum):
    NONE = 0
    IN = 1
    OUT = 2
    BOTH = 3

    def has(self, other):
        """
        Check whether this Direction contains Direction other.
        `other` A `Direction` to compare against.
        Returns True if this is BOTH and other is not NONE, otherwise False
        """
        if self is Direction.BOTH:
            return other is not Direction.NONE
        else:
            return self is other

    def __add__(self, other):
        return Direction(self.value | other.value)

    def __sub__(self, other):
        return Direction(self.value - (self.value and other.value))

    @property
    def short_name(self):
        return str(self)[10:]
