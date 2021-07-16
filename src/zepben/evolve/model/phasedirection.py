#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum

__all__ = ["PhaseDirection", "phasedirection_from_value"]


class PhaseDirection(Enum):
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
        if self is PhaseDirection.BOTH:
            return other is not PhaseDirection.NONE
        else:
            return self is other

    def __add__(self, other):
        return PhaseDirection(self.value | other.value)

    def __sub__(self, other):
        return PhaseDirection(self.value - (self.value and other.value))

    @property
    def short_name(self):
        return str(self)[15:]


def phasedirection_from_value(value: int) -> PhaseDirection:
    if 0 <= value <= 3:
        return PhaseDirection.NONE
    else:
        PhaseDirection(value)
