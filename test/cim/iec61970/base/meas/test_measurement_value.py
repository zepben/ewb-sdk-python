#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.ewb.model.cim.iec61970.base.meas.measurement_value import MeasurementValue


def verify_measurement_value_constructor_default(mv: MeasurementValue):
    assert not mv.time_stamp


def verify_measurement_value_constructor_kwargs(mv: MeasurementValue, time_stamp, **kwargs):
    assert not kwargs
    assert mv.time_stamp == time_stamp
