#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0.

__all__ = ["DependencyKind"]

from enum import Enum

from zepben.ewb import unique


@unique
class DependencyKind(Enum):
    """
    Enum describing the different relationships two objects may have.
    """

    UNKNOWN = 0
    """Default, unknown."""

    mutuallyExclusive = 1
    """The dependencies cannot exist together."""

    required = 2
    """The dependencies must exist together."""

    @property
    def short_name(self) -> str:
        """Get the name of this `DependencyKind` without the class qualifier."""
        return str(self)[15:]
