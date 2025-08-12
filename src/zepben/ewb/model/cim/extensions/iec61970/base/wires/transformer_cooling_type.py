#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TransformerCoolingType"]

from enum import Enum

from zepben.ewb import unique
from zepben.ewb.model.cim.extensions.zbex import zbex


@zbex
@unique
class TransformerCoolingType(Enum):
    """
    [ZBEX]
    Transformer cooling types.
    """

    UNKNOWN = 0
    """[ZBEX] Default"""

    ONAN = 1
    """[ZBEX] Oil natural, air natural"""

    ONAF = 2
    """[ZBEX] Oil natural, air forced"""

    OFAF = 3
    """[ZBEX] Oil forced, air forced"""

    OFWF = 4
    """[ZBEX] Oil forced, water forced"""

    ODAF = 5
    """[ZBEX] Oil directed, air forced"""

    KNAN = 6
    """[ZBEX] Non-mineral oil natural, air natural"""

    KNAF = 7
    """[ZBEX] Non-mineral oil natural, air forced"""

    KFAF = 8
    """[ZBEX] Non-mineral oil forced, air forced"""

    KFWF = 9
    """[ZBEX] Non-mineral oil forced, water forced"""

    KDAF = 10
    """[ZBEX] Non-mineral oil directed, air forced"""

    @property
    def short_name(self):
        return str(self)[23:]
