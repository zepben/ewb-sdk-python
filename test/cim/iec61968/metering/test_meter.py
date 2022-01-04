#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import data

from cim.common_testing_functions import verify
from test.cim.iec61968.metering.test_end_device import end_device_kwargs, verify_end_device_constructor_default, verify_end_device_constructor_kwargs, \
    verify_end_device_constructor_args, end_device_args
from zepben.evolve import Meter, UsagePoint
from zepben.evolve.model.cim.iec61968.metering.create_metering_components import create_meter

meter_kwargs = end_device_kwargs
meter_args = end_device_args


def test_meter_constructor_default():
    verify_end_device_constructor_default(Meter())
    verify_end_device_constructor_default(create_meter())


# noinspection PyShadowingNames
@given(data())
def test_meter_constructor_kwargs(data):
    verify(
        [Meter, create_meter],
        data, meter_kwargs, verify_end_device_constructor_kwargs
    )


def test_meter_constructor_args():
    # noinspection PyArgumentList
    verify_end_device_constructor_args(Meter(*meter_args))


def test_auto_two_way_connections_for_meter_constructor():
    up = UsagePoint()
    m = create_meter(usage_points=[up])

    assert up.get_end_device(m.mrid) == m
