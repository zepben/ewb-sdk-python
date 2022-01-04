#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import data

from test.cim.common_testing_functions import verify
from test.cim.iec61970.base.meas.test_measurement import measurement_kwargs, verify_measurement_constructor_default, \
    verify_measurement_constructor_kwargs, verify_measurement_constructor_args, measurement_args
from zepben.evolve import Analog, RemoteSource
from zepben.evolve.model.cim.iec61970.base.meas.create_meas_components import create_analog

analog_kwargs = measurement_kwargs
analog_args = measurement_args


def test_analog_constructor_default():
    verify_measurement_constructor_default(Analog())
    verify_measurement_constructor_default(create_analog())


# noinspection PyShadowingNames
@given(data())
def test_analog_constructor_kwargs(data):
    verify(
        [Analog, create_analog],
        data, analog_kwargs, verify_measurement_constructor_kwargs
    )


def test_analog_constructor_args():
    # noinspection PyArgumentList
    verify_measurement_constructor_args(Analog(*analog_args))


def test_auto_two_way_connections_for_analog_constructor():
    rs = RemoteSource()
    a = create_analog(remote_source=rs)

    assert rs.measurement == a
