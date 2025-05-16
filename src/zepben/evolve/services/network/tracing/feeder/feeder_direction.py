#  Copyright 2024 Zeppelin Bend Pty Ltd
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

    CONNECTOR = 4
    """
    The terminal belongs to a Connector that is modelled with only a single terminal.
    CONNECTOR will match direction UPSTREAM, DOWNSTREAM, and BOTH, however it exists
    to differentiate it from BOTH which is used to indicate loops on the feeder. This
    however means you connected tell if a terminal with CONNECTOR is part of a loop
    directly, you need to check its connected terminals and check for BOTH to determine
    if it is in a loop.
    """

    def __contains__(self, other):
        """
        Check whether this `FeederDirection`` contains another `FeederDirection`.

        :param other: The `FeederDirection` to check.
        :return: `True` if this is `BOTH` and other is not `NONE`, or if the directions are the same, otherwise `False`
        """
        if self in (FeederDirection.BOTH, FeederDirection.CONNECTOR):
            return other is not FeederDirection.NONE
        else:
            return self is other

    def __add__(self, other):
        """
        Add a `FeederDirection` to this `FeederDirection`

        :param other: The `FeederDirection` to add.
        :return: The resulting `FeederDirection` with `other` added.
        """
        if self == FeederDirection.CONNECTOR:
            return FeederDirection.CONNECTOR

        return FeederDirection(self.value | other.value)

    def __sub__(self, other):
        """
        Remove a `FeederDirection` from this `FeederDirection`

        :param other: The `FeederDirection` to remove.
        :return: The resulting `FeederDirection` with `other` removed.
        """
        if self == FeederDirection.CONNECTOR:
            return FeederDirection.CONNECTOR

        return FeederDirection(self.value - (self.value & other.value))

    def __invert__(self):
        if self == FeederDirection.UPSTREAM:
            return FeederDirection.DOWNSTREAM
        elif self == FeederDirection.DOWNSTREAM:
            return FeederDirection.UPSTREAM
        elif self in (FeederDirection.BOTH, FeederDirection.CONNECTOR):
            return FeederDirection.NONE
        else:  # lif self == FeederDirection.NONE:
            return FeederDirection.BOTH

    @property
    def complementary_external_direction(self):
        if self == FeederDirection.UPSTREAM:
            return FeederDirection.DOWNSTREAM
        elif self == FeederDirection.DOWNSTREAM:
            return FeederDirection.UPSTREAM
        else:
            return self

    @property
    def short_name(self) -> str:
        """
        :return: The name of the enum without the class name.
        """
        return str(self)[16:]
