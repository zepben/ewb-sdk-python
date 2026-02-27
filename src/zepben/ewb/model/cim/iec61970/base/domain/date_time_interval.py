#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.4

__all__ = ["DateTimeInterval"]

from dataclasses import dataclass
from datetime import datetime

from zepben.ewb import require


@dataclass
class DateTimeInterval:
    """
    Interval between two date and time points, where the interval includes the start time but excludes end time.

    :var start: Start date and time of this interval. The start date and time is included in the defined interval.
    :var end: End date and time of this interval. The end date and time where the interval is defined up to, but excluded.
    """
    start: datetime | None = None
    """Start date and time of this interval. The start date and time is included in the defined interval."""

    end: datetime | None = None
    """End date and time of this interval. The end date and time where the interval is defined up to, but excluded."""

    def __post_init__(self):
        require(any((self.start, self.end)), lambda: 'You must provide a start or end time.')
        if all((self.start, self.end)):
            require(self.start <= self.end, lambda: 'The start time must be before the end time.')
