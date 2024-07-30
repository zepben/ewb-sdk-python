#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from enum import Enum

__all__ = ["PowerDirectionKind"]


class PowerDirectionKind(Enum):
    """The flow of power direction used by a ProtectionEquipment."""

    UNKNOWN_DIRECTION = 0
    """Unknown power direction flow."""

    UNDIRECTED = 1
    """Power direction flow type is not specified."""

    FORWARD = 2
    """Power direction forward flow is used."""

    REVERSE = 3
    """Power direction reverse flow is used."""

    @property
    def short_name(self):
        return str(self)[19:]
