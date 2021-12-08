#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given

from test.cim.iec61968.metering.test_end_device import end_device_kwargs, verify_end_device_constructor_default, verify_end_device_constructor_kwargs, \
    verify_end_device_constructor_args, end_device_args
from zepben.evolve import Meter
from zepben.evolve.model.cim.iec61968.metering.create_metering_components import create_meter

meter_kwargs = end_device_kwargs
meter_args = end_device_args


def test_meter_constructor_default():
    verify_end_device_constructor_default(Meter())
    verify_end_device_constructor_default(create_meter())


@given(**meter_kwargs)
def test_meter_constructor_kwargs(**kwargs):
    # noinspection PyArgumentList
    verify_end_device_constructor_kwargs(Meter(**kwargs), **kwargs)


@given(**meter_kwargs)
def test_meter_creator(**kwargs):
    # noinspection PyArgumentList
    verify_end_device_constructor_kwargs(create_meter(**kwargs), **kwargs)


def test_meter_constructor_args():
    # noinspection PyArgumentList
    verify_end_device_constructor_args(Meter(*meter_args))
