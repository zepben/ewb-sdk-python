#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum

__all__ = ["FeederDirection"]


class FeederDirection(Enum):
    """
    Enumeration of directions along a feeder at a terminal.
    """

    NONE = 0
    """
    The terminal is not on a feeder.
    """

    UPSTREAM = 1
    """
    The terminal can be used to trace upstream towards the feeder head.
    """

    DOWNSTREAM = 2
    """
    The terminal can be used to trace downstream away from the feeder head.
    """

    BOTH = 3
    """
    The terminal is part of a loop on the feeder and tracing in either direction will allow you
    to trace upstream towards the feeder head, or downstream away from the feeder head.
    """

    # todo replace .has(
    def __contains__(self, other):
        """
        Check whether this `FeederDirection`` contains another `FeederDirection`.

        :param other: The `FeederDirection` to check.
        :return: `True` if this is `BOTH` and other is not `NONE`, or if the directions are the same, otherwise `False`
        """
        if self is FeederDirection.BOTH:
            return other is not FeederDirection.NONE
        else:
            return self is other

    def __add__(self, other):
        """
        Add a `FeederDirection` to this `FeederDirection`

        :param other: The `FeederDirection` to add.
        :return: The resulting `FeederDirection` with `other` added.
        """
        return FeederDirection(self.value | other.value)

    def __sub__(self, other):
        """
        Remove a `FeederDirection` from this `FeederDirection`

        :param other: The `FeederDirection` to remove.
        :return: The resulting `FeederDirection` with `other` removed.
        """
        return FeederDirection(self.value - (self.value & other.value))

    def __invert__(self):
        if self == FeederDirection.UPSTREAM:
            return FeederDirection.DOWNSTREAM
        elif self == FeederDirection.DOWNSTREAM:
            return FeederDirection.UPSTREAM
        elif self == FeederDirection.BOTH:
            return FeederDirection.NONE
        else:  # lif self == FeederDirection.NONE:
            return FeederDirection.BOTH

    @property
    def short_name(self) -> str:
        """
        :return: The name of the enum without the class name.
        """
        return str(self)[16:]
