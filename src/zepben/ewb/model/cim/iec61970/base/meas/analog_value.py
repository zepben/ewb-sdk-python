#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["AnalogValue"]

from typing import Optional

from zepben.ewb.model.cim.iec61970.base.meas.measurement_value import MeasurementValue


class AnalogValue(MeasurementValue):
    """`AnalogValue` represents an analog `MeasurementValue`."""

    value: float = 0.0
    """The value to supervise"""

    analog_mrid: Optional[str] = None
    """The `zepben.ewb.model.cim.iec61970.base.meas.measurement.Analog` mRID of this `AnalogValue`"""
