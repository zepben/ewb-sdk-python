

#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum

__all__ = ["DiagramStyle"]


class DiagramStyle(Enum):
    """
    The diagram style refer to a style used by the originating system for a diagram.  A diagram style describes
    information such as schematic, geographic, bus-branch etc.
    """

    SCHEMATIC = 0
    """The diagram should be styled as a schematic view."""

    GEOGRAPHIC = 1
    """The diagram should be styled as a geographic view."""

    @property
    def short_name(self):
        return str(self)[13:]
