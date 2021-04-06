#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from enum import Enum

__all__ = ["BatteryStateKind"]


class BatteryStateKind(Enum):
    """Battery state"""
    
    UNKNOWN = 0
    """Battery state is not known."""

    discharging = 1
    """Stored energy is decreasing."""

    full = 2
    """Unable to charge, and not discharging."""

    waiting = 3
    """Neither charging nor discharging, but able to do so."""

    charging = 4
    """Stored energy is increasing."""

    empty = 5
    """Unable to discharge, and not charging."""

    @property
    def short_name(self):
        return str(self)[17:]
