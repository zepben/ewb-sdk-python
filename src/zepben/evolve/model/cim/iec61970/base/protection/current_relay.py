#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional

from zepben.evolve.model.cim.iec61970.base.protection.protection_relay_function import ProtectionRelayFunction

__all__ = ["CurrentRelay"]


class CurrentRelay(ProtectionRelayFunction):
    """A device that checks current flow values in any direction or designated direction."""

    current_limit_1: Optional[float] = None
    """Current limit number 1 for inverse time pickup in amperes."""

    inverse_time_flag: Optional[bool] = None
    """Set true if the current relay has inverse time characteristic."""

    time_delay_1: Optional[float] = None
    """Inverse time delay number 1 for current limit number 1 in seconds."""
