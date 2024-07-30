#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from enum import Enum

__all__ = ["RegulatingControlModeKind"]


class RegulatingControlModeKind(Enum):
    """The kind of regulation model. For example regulating voltage, reactive power, active power, etc."""

    UNKNOWN_CONTROL_MODE = 0
    """Default, unknown."""

    voltage = 1
    """Voltage is specified."""

    activePower = 2
    """Active power is specified."""

    reactivePower = 3
    """Reactive power is specified."""

    currentFlow = 4
    """Current flow is specified."""

    admittance = 5
    """Admittance is specified."""

    timeScheduled = 6
    """Control switches on/off by time of day. The times may change on the weekend, or in different seasons."""

    temperature = 7
    """Control switches on/off based on the local temperature (i.e., a thermostat)."""

    powerFactor = 8
    """Power factor is specified."""

    @property
    def short_name(self):
        return str(self)[26:]
