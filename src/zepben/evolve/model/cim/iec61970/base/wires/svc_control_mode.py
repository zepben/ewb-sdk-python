#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

__all__ = ["SVCControlMode"]


class SVCControlMode(Enum):
    """
    Static VAr Compensator control mode.
    """

    UNKNOWN = 0
    """[ZBEX] Unknown control."""

    reactivePower = 1
    """Reactive power control."""

    voltage = 2
    """Voltage control."""

    @property
    def short_name(self):
        return str(self)[15:]
