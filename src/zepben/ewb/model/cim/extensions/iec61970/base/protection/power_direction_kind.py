#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["PowerDirectionKind"]

from enum import Enum

from zepben.ewb.model.cim.extensions.zbex import zbex
from zepben.ewb.util import unique


@zbex
@unique
class PowerDirectionKind(Enum):
    """
    [ZBEX]
    The flow of power direction used by a ProtectionEquipment.
    """

    UNKNOWN = 0
    """[ZBEX] Unknown power direction flow."""

    UNDIRECTED = 1
    """[ZBEX] Power direction flow type is not specified."""

    FORWARD = 2
    """[ZBEX] Power direction forward flow is used."""

    REVERSE = 3
    """[ZBEX] Power direction reverse flow is used."""

    @property
    def short_name(self):
        return str(self)[19:]
