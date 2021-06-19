#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum

__all__ = ["DiagramObjectStyle"]


class DiagramObjectStyle(Enum):
    """
    The diagram style refer to a style used by the originating system for a diagram.  A diagram style describes
    information such as schematic, geographic, bus-branch etc.
    """

    NONE = 0
    """No specific styling should be applied."""

    DIST_TRANSFORMER = 1
    """Diagram object should be styled as a distribution transformer."""

    ISO_TRANSFORMER = 2
    """Diagram object should be styled as an isolating transformer."""

    REVERSIBLE_REGULATOR = 3
    """Diagram object should be styled as a reversible regulator transformer."""

    NON_REVERSIBLE_REGULATOR = 4
    """Diagram object should be styled as a non-reversiable transformer."""

    ZONE_TRANSFORMER = 5
    """Diagram object should be styled as a zone transformer."""

    FEEDER_CB = 6
    """Diagram object should be styled as a feeder circuit breaker."""

    CB = 7
    """Diagram object should be styled as a circuit breaker."""

    JUNCTION = 8
    """Diagram object should be styled as a junction."""

    SWITCH = 9
    """Diagram object should be styled as a generic switch."""

    ARC_CHUTE = 10
    """Diagram object should be styled as an ARC chute."""

    BRIDGE = 11
    """Diagram object should be styled as a broken bridge."""

    DISCONNECTOR = 12
    """Diagram object should be styled as a disconnector."""

    FLICKER_BLADE = 13
    """Diagram object should be styled as a flicker blade switch."""

    FUSE = 14
    """Diagram object should be styled as a fuse."""

    GAS_INSULATED = 15
    """Diagram object should be styled as a gas insulated switch."""

    LIVE_LINE_CLAMP = 16
    """Diagram object should be styled as a live line clamp."""

    RECLOSER = 17
    """Diagram object should be styled as a recloser."""

    FAULT_INDICATOR = 18
    """Diagram object should be styled as a fault indicator."""

    JUMPER = 19
    """Diagram object should be styled as a jumper."""

    ENERGY_SOURCE = 20
    """Diagram object should be styled as a energy source."""

    SHUNT_COMPENSATOR = 21
    """Diagram object should be styled as a shunt compensator."""

    USAGE_POINT = 22
    """Diagram object should be styled as a usage point."""

    CONDUCTOR_UNKNOWN = 23
    """Diagram object should be styled as a conductor at unknown voltage."""

    CONDUCTOR_LV = 24
    """Diagram object should be styled as a conductor at low voltage."""

    CONDUCTOR_6600 = 25
    """Diagram object should be styled as a conductor at 6.6kV."""

    CONDUCTOR_11000 = 26
    """Diagram object should be styled as a conductor at 11kV."""

    CONDUCTOR_12700 = 27
    """Diagram object should be styled as a conductor at 12.7kV (SWER)."""

    CONDUCTOR_22000 = 28
    """Diagram object should be styled as a conductor at 22kV."""

    CONDUCTOR_33000 = 29
    """Diagram object should be styled as a conductor at 33kV."""

    CONDUCTOR_66000 = 30
    """Diagram object should be styled as a conductor at 66kV."""

    CONDUCTOR_132000 = 31
    """Diagram object should be styled as a conductor at 132kV."""

    CONDUCTOR_220000 = 32
    """Diagram object should be styled as a conductor at 220kV."""

    CONDUCTOR_275000 = 33
    """Diagram object should be styled as a conductor at 275kV."""

    CONDUCTOR_500000 = 34
    """Diagram object should be styled as a conductor at 500kV."""

    POWER_ELECTRONICS_CONNECTION = 35
    """Diagram object should be styled as a power electronics connection."""

    BATTERY_UNIT = 36
    """Diagram object should be styled as a battery unit."""

    PHOTO_VOLTAIC_UNIT = 37
    """Diagram object should be styled as a photo voltaic unit."""

    POWER_ELECTRONICS_WIND_UNIT = 38
    """Diagram object should be styled as a power electronics wind unit."""

    def is_line_style(self) -> bool:
        return self.short_name.startswith("CONDUCTOR_")

    @property
    def short_name(self):
        return str(self)[19:]
