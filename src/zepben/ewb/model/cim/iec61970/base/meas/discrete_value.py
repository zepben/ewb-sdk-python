#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["DiscreteValue"]

from zepben.ewb.dataslot import dataslot
from zepben.ewb.model.cim.iec61970.base.meas.measurement_value import MeasurementValue


@dataslot
class DiscreteValue(MeasurementValue):
    """`DiscreteValue` represents a discrete `MeasurementValue`."""

    value: int = 0
    """The value to supervise"""

    discrete_mrid: str | None = None
    """The `zepben.ewb.model.cim.iec61970.base.meas.measurement.Discrete` mRID of this `DiscreteValue`"""
