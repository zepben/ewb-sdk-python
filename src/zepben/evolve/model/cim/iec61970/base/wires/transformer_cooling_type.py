#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from enum import Enum

__all__ = ["TransformerCoolingType"]


class TransformerCoolingType(Enum):
    """Transformer cooling types."""

    UNKNOWN_COOLING_TYPE = 0
    """Default"""

    ONAN = 1
    """Oil natural, air natural"""

    ONAF = 2
    """Oil natural, air forced"""

    OFAF = 3
    """Oil forced, air forced"""

    OFWF = 4
    """Oil forced, water forced"""

    ODAF = 5
    """Oil directed, air forced"""

    KNAN = 6
    """Non-mineral oil natural, air natural"""

    KNAF = 7
    """Non-mineral oil natural, air forced"""

    KFAF = 8
    """Non-mineral oil forced, air forced"""

    KFWF = 9
    """Non-mineral oil forced, water forced"""

    KDAF = 10
    """ Non-mineral oil directed, air forced"""

    @property
    def short_name(self):
        return str(self)[23:]
