#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from test.cim.iec61970.base.meas.test_measurement import measurement_kwargs, verify_measurement_constructor_default, \
    verify_measurement_constructor_kwargs, verify_measurement_constructor_args, measurement_args
from zepben.evolve import Analog
from zepben.evolve.model.cim.iec61970.base.meas.create_meas_components import create_analog

analog_kwargs = measurement_kwargs
analog_args = measurement_args


def test_analog_constructor_default():
    verify_measurement_constructor_default(Analog())
    verify_measurement_constructor_default(create_analog())


@given(**analog_kwargs)
def test_analog_constructor_kwargs(**kwargs):
    # noinspection PyArgumentList
    verify_measurement_constructor_kwargs(Analog(**kwargs), **kwargs)


@given(**analog_kwargs)
def test_analog_creator(**kwargs):
    # noinspection PyArgumentList
    verify_measurement_constructor_kwargs(create_analog(**kwargs), **kwargs)


def test_analog_constructor_args():
    # noinspection PyArgumentList
    verify_measurement_constructor_args(Analog(*analog_args))
