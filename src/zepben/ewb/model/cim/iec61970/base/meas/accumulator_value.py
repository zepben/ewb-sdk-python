#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["AccumulatorValue"]

from typing import Optional

from zepben.ewb.model.cim.iec61970.base.meas.measurement_value import MeasurementValue


class AccumulatorValue(MeasurementValue):
    """AccumulatorValue represents an accumulated (counted) MeasurementValue."""

    value: int = 0
    """The value to supervise"""

    accumulator_mrid: Optional[str] = None
    """The `zepben.ewb.model.cim.iec61970.base.meas.measurement.Accumulator` mRID of this `AccumulatorValue`"""
