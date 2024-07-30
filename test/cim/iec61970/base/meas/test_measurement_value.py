#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import datetime

from hypothesis.strategies import datetimes

from zepben.evolve import MeasurementValue

measurement_value_kwargs = {"time_stamp": datetimes()}
measurement_value_args = [datetime(2021, 1, 1)]


def verify_measurement_value_constructor_default(mv: MeasurementValue):
    assert not mv.time_stamp


def verify_measurement_value_constructor_kwargs(mv: MeasurementValue, time_stamp, **kwargs):
    assert not kwargs
    assert mv.time_stamp == time_stamp


def verify_measurement_value_constructor_args(mv: MeasurementValue):
    assert mv.time_stamp == measurement_value_args[-1]
