#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from enum import Enum

__all__ = ["ProtectionKind"]


class ProtectionKind(Enum):
    """The kind of protection being provided by this protection equipment."""

    UNKNOWN = 0
    """Unknown"""

    EF = 1
    """Earth Fault"""

    SEF = 2
    """Sensitive Earth Fault"""

    OC = 3
    """Overcurrent"""

    IOC = 4
    """Instantaneous Overcurrent"""

    IEF = 5
    """Instantaneous Earth Fault"""

    REF = 6
    """Restricted Earth Fault"""

    @property
    def short_name(self):
        return str(self)[15:]
