#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from datetime import datetime
from typing import Optional

from dataclassy import dataclass

__all__ = ["MeasurementValue", "AccumulatorValue", "AnalogValue", "DiscreteValue"]


@dataclass(slots=True)
class MeasurementValue(object):
    """
    The current state for a measurement. A state value is an instance of a measurement from a specific source.
    Measurements can be associated with many state values, each representing a different source for the measurement.
    """
    time_stamp: Optional[datetime] = None
    """The time when the value was last updated."""


class AccumulatorValue(MeasurementValue):
    """AccumulatorValue represents an accumulated (counted) MeasurementValue."""

    value: int = 0
    """The value to supervise"""

    accumulator_mrid: Optional[str] = None
    """The `zepben.evolve.cim.iec61970.base.meas.measurement.Accumulator` mRID of this `AccumulatorValue`"""


class AnalogValue(MeasurementValue):
    """`AnalogValue` represents an analog `MeasurementValue`."""

    value: float = 0.0
    """The value to supervise"""

    analog_mrid: Optional[str] = None
    """The `zepben.evolve.cim.iec61970.base.meas.measurement.Analog` mRID of this `AnalogValue`"""


class DiscreteValue(MeasurementValue):
    """`DiscreteValue` represents a discrete `MeasurementValue`."""

    value: int = 0
    """The value to supervise"""

    discrete_mrid: Optional[str] = None
    """The `zepben.evolve.cim.iec61970.base.meas.measurement.Discrete` mRID of this `DiscreteValue`"""
