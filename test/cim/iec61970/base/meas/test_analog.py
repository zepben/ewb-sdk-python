#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.fill_fields import analog_kwargs
from cim.iec61970.base.meas.test_measurement import verify_measurement_constructor_default, \
    verify_measurement_constructor_kwargs, verify_measurement_constructor_args, measurement_args
from zepben.ewb import generate_id
from zepben.ewb.model.cim.iec61970.base.meas.analog import Analog

analog_args = measurement_args


def test_analog_constructor_default():
    analog = Analog(mrid=generate_id())
    verify_measurement_constructor_default(analog)

    assert analog.positive_flow_in is None


@given(**analog_kwargs())
def test_analog_constructor_kwargs(positive_flow_in, **kwargs):
    ana = Analog(
        positive_flow_in=positive_flow_in,
        **kwargs
    )

    verify_measurement_constructor_kwargs(ana, **kwargs)
    assert ana.positive_flow_in == positive_flow_in


def test_analog_constructor_args():
    verify_measurement_constructor_args(Analog(*analog_args))
