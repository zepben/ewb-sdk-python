

#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum, auto

__all__ = ["DiagramObjectStyle"]


class DiagramObjectStyle(Enum):
    """
    The diagram style refer to a style used by the originating system for a diagram.  A diagram style describes
    information such as schematic, geographic, bus-branch etc.
    """

    NONE = (auto(), False)
    """No specific styling should be applied."""

    DIST_TRANSFORMER = (auto(), False)
    """Diagram object should be styled as a distribution transformer."""

    ISO_TRANSFORMER = (auto(), False)
    """Diagram object should be styled as an isolating transformer."""

    REVERSIBLE_REGULATOR = (auto(), False)
    """Diagram object should be styled as a reversible regulator transformer."""

    NON_REVERSIBLE_REGULATOR = (auto(), False)
    """Diagram object should be styled as a non-reversiable transformer."""

    ZONE_TRANSFORMER = (auto(), False)
    """Diagram object should be styled as a zone transformer."""

    FEEDER_CB = (auto(), False)
    """Diagram object should be styled as a feeder circuit breaker."""

    CB = (auto(), False)
    """Diagram object should be styled as a circuit breaker."""

    JUNCTION = (auto(), False)
    """Diagram object should be styled as a junction."""

    DISCONNECTOR = (auto(), False)
    """Diagram object should be styled as a disconnector."""

    FUSE = (auto(), False)
    """Diagram object should be styled as a fuse."""

    RECLOSER = (auto(), False)
    """Diagram object should be styled as a recloser."""

    FAULT_INDICATOR = (auto(), False)
    """Diagram object should be styled as a fault indicator."""

    JUMPER = (auto(), False)
    """Diagram object should be styled as a jumper."""

    ENERGY_SOURCE = (auto(), False)
    """Diagram object should be styled as a energy source."""

    SHUNT_COMPENSATOR = (auto(), False)
    """Diagram object should be styled as a shunt compensator."""

    USAGE_POINT = (auto(), False)
    """Diagram object should be styled as a usage point."""

    CONDUCTOR_UNKNOWN = (auto(), True)
    """Diagram object should be styled as a conductor at unknown voltage."""

    CONDUCTOR_LV = (auto(), True)
    """Diagram object should be styled as a conductor at low voltage."""

    CONDUCTOR_6600 = (auto(), True)
    """Diagram object should be styled as a conductor at 6.6kV."""

    CONDUCTOR_11000 = (auto(), True)
    """Diagram object should be styled as a conductor at 11kV."""

    CONDUCTOR_12700 = (auto(), True)
    """Diagram object should be styled as a conductor at 12.7kV (SWER)."""

    CONDUCTOR_22000 = (auto(), True)
    """Diagram object should be styled as a conductor at 22kV."""

    CONDUCTOR_33000 = (auto(), True)
    """Diagram object should be styled as a conductor at 33kV."""

    CONDUCTOR_66000 = (auto(), True)
    """Diagram object should be styled as a conductor at 66kV."""

    CONDUCTOR_132000 = (auto(), True)
    """Diagram object should be styled as a conductor at 132kV."""

    CONDUCTOR_220000 = (auto(), True)
    """Diagram object should be styled as a conductor at 220kV."""

    CONDUCTOR_275000 = (auto(), True)
    """Diagram object should be styled as a conductor at 275kV."""

    CONDUCTOR_500000 = (auto(), True)
    """Diagram object should be styled as a conductor at 500kV or above."""

    def is_line_style(self) -> bool:
        return self.value[1]

    @property
    def short_name(self):
        return str(self)[16:]
