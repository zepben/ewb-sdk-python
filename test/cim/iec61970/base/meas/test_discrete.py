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
from zepben.evolve import Discrete, RemoteSource
from zepben.evolve.model.cim.iec61970.base.meas.create_meas_components import create_discrete

discrete_kwargs = measurement_kwargs
discrete_args = measurement_args


def test_discrete_constructor_default():
    verify_measurement_constructor_default(Discrete())
    verify_measurement_constructor_default(create_discrete())


# noinspection PyShadowingNames
@given(data())
def test_discrete_constructor_kwargs(data):
    verify(
        [Discrete, create_discrete],
        data, discrete_kwargs, verify_measurement_constructor_kwargs
    )


def test_discrete_constructor_args():
    # noinspection PyArgumentList
    verify_measurement_constructor_args(Discrete(*discrete_args))


def test_auto_two_way_connections_for_discrete_constructor():
    rs = RemoteSource()
    d = create_discrete(remote_source=rs)

    assert rs.measurement == d
