#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["MeasurementValue"]

from datetime import datetime
from typing import Optional

from zepben.ewb.dataclassy import dataclass


@dataclass(slots=True)
class MeasurementValue(object):
    """
    The current state for a measurement. A state value is an instance of a measurement from a specific source.
    Measurements can be associated with many state values, each representing a different source for the measurement.
    """
    time_stamp: Optional[datetime] = None
    """The time when the value was last updated."""
