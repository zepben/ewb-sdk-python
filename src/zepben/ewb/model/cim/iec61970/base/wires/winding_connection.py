#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["WindingConnection"]

from enum import Enum

from zepben.ewb import unique


@unique
class WindingConnection(Enum):
    """
    Winding connection type.
    """

    UNKNOWN = 0
    """Default"""

    D = 1
    """Delta"""

    Y = 2
    """Wye"""

    Z = 3
    """ZigZag"""

    Yn = 4
    """Wye, with neutral brought out for grounding"""

    Zn = 5
    """ZigZag, with neutral brought out for grounding"""

    A = 6
    """Autotransformer common winding"""

    I = 7
    """Independent winding, for single-phase connections"""

    @property
    def short_name(self):
        return str(self)[18:]
