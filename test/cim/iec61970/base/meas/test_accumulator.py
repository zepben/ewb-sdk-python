#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import data

from cim.common_testing_functions import verify
from test.cim.iec61970.base.meas.test_measurement import measurement_kwargs, verify_measurement_constructor_default, \
    verify_measurement_constructor_kwargs, verify_measurement_constructor_args, measurement_args
from zepben.evolve import Accumulator, RemoteSource
from zepben.evolve.model.cim.iec61970.base.meas.create_meas_components import create_accumulator

accumulator_kwargs = measurement_kwargs
accumulator_args = measurement_args


def test_accumulator_constructor_default():
    verify_measurement_constructor_default(Accumulator())
    verify_measurement_constructor_default(create_accumulator())


# noinspection PyShadowingNames
@given(data())
def test_accumulator_constructor_kwargs(data):
    verify(
        [Accumulator, create_accumulator],
        data, accumulator_kwargs, verify_measurement_constructor_kwargs
    )


def test_accumulator_constructor_args():
    # noinspection PyArgumentList
    verify_measurement_constructor_args(Accumulator(*accumulator_args))


def test_auto_two_way_connections_for_accumulator_constructor():
    rs = RemoteSource()
    a = create_accumulator(remote_source=rs)

    assert rs.measurement == a
