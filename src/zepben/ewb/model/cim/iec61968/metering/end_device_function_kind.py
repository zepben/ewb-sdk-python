#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["EndDeviceFunctionKind"]

from enum import Enum

from zepben.ewb import unique


@unique
class EndDeviceFunctionKind(Enum):
    """
    Kind of end device function.
    """

    UNKNOWN = 0
    """Unknown function kind."""

    autonomousDst = 1
    """Autonomous application of daylight saving time (DST)."""

    demandResponse = 2
    """Demand response functions."""

    electricMetering = 3
    """Electricity metering."""

    metrology = 4
    """Presentation of metered values to a user or another system (always a function of a meter, but might not be supported by a load control unit)."""

    onRequestRead = 5
    """On-request reads."""

    outageHistory = 6
    """Reporting historical power interruption data."""

    relaysProgramming = 7
    """Support for one or more relays that may be programmable in the meter (and tied to TOU, time pulse, load control or other functions)."""

    reverseFlow = 8
    """Detection and monitoring of reverse flow."""

    @property
    def short_name(self):
        return str(self)[22:]
