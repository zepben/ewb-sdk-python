"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""

from enum import Enum, auto

__all__ = ["DiagramObjectStyle"]


class DiagramObjectStyle(Enum):
    """
    The diagram style refer to a style used by the originating system for a diagram.  A diagram style describes
    information such as schematic, geographic, bus-branch etc.
    """

    # No specific styling should be applied.
    NONE = (auto(), False)

    # Diagram object should be styled as a distribution transformer.
    DIST_TRANSFORMER = (auto(), False)

    # Diagram object should be styled as an isolating transformer.
    ISO_TRANSFORMER = (auto(), False)

    # Diagram object should be styled as a reversible regulator transformer.
    REVERSIBLE_REGULATOR = (auto(), False)

    # Diagram object should be styled as a non-reversiable transformer.
    NON_REVERSIBLE_REGULATOR = (auto(), False)

    # Diagram object should be styled as a zone transformer.
    ZONE_TRANSFORMER = (auto(), False)

    # Diagram object should be styled as a feeder circuit breaker.
    FEEDER_CB = (auto(), False)

    # Diagram object should be styled as a circuit breaker.
    CB = (auto(), False)

    # Diagram object should be styled as a junction.
    JUNCTION = (auto(), False)

    # Diagram object should be styled as a disconnector.
    DISCONNECTOR = (auto(), False)

    # Diagram object should be styled as a fuse.
    FUSE = (auto(), False)

    # Diagram object should be styled as a recloser.
    RECLOSER = (auto(), False)

    # Diagram object should be styled as a fault indicator.
    FAULT_INDICATOR = (auto(), False)

    # Diagram object should be styled as a jumper.
    JUMPER = (auto(), False)

    # Diagram object should be styled as a energy source.
    ENERGY_SOURCE = (auto(), False)

    # Diagram object should be styled as a shunt compensator.
    SHUNT_COMPENSATOR = (auto(), False)

    # Diagram object should be styled as a usage point.
    USAGE_POINT = (auto(), False)

    # Diagram object should be styled as a conductor at unknown voltage.
    CONDUCTOR_UNKNOWN = (auto(), True)

    # Diagram object should be styled as a conductor at low voltage.
    CONDUCTOR_LV = (auto(), True)

    # Diagram object should be styled as a conductor at 6.6kV.
    CONDUCTOR_6600 = (auto(), True)

    # Diagram object should be styled as a conductor at 11kV.
    CONDUCTOR_11000 = (auto(), True)

    # Diagram object should be styled as a conductor at 12.7kV (SWER).
    CONDUCTOR_12700 = (auto(), True)

    # Diagram object should be styled as a conductor at 22kV.
    CONDUCTOR_22000 = (auto(), True)

    # Diagram object should be styled as a conductor at 33kV.
    CONDUCTOR_33000 = (auto(), True)

    # Diagram object should be styled as a conductor at 66kV.
    CONDUCTOR_66000 = (auto(), True)

    # Diagram object should be styled as a conductor at 132kV.
    CONDUCTOR_132000 = (auto(), True)

    # Diagram object should be styled as a conductor at 220kV.
    CONDUCTOR_220000 = (auto(), True)

    # Diagram object should be styled as a conductor at 275kV.
    CONDUCTOR_275000 = (auto(), True)

    # Diagram object should be styled as a conductor at 500kV or above.
    CONDUCTOR_500000 = (auto(), True)

    def is_line_style(self) -> bool:
        return self.value[1]

    @property
    def short_name(self):
        return str(self)[16:]
