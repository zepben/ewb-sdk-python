#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, data

from test.cim.common_testing_functions import verify
from test.cim.iec61970.base.scada.test_remote_point import remote_point_kwargs, verify_remote_point_constructor_default, \
    verify_remote_point_constructor_kwargs, verify_remote_point_constructor_args, remote_point_args
from zepben.evolve import RemoteSource, Measurement
from zepben.evolve.model.cim.iec61970.base.scada.create_scada_components import create_remote_source

remote_source_kwargs = {
    **remote_point_kwargs,
    "measurement": builds(Measurement)
}

remote_source_args = [*remote_point_args, Measurement()]


def test_remote_source_constructor_default():
    rs = RemoteSource()
    rs2 = create_remote_source()
    verify_default_remote_source_constructor(rs)
    verify_default_remote_source_constructor(rs2)


def verify_default_remote_source_constructor(rs):
    verify_remote_point_constructor_default(rs)
    assert not rs.measurement


# noinspection PyShadowingNames
@given(data())
def test_remote_source_constructor_kwargs(data):
    verify(
        [RemoteSource, create_remote_source],
        data, remote_source_kwargs, verify_remote_source_values
    )


def verify_remote_source_values(rs, measurement, **kwargs):
    verify_remote_point_constructor_kwargs(rs, **kwargs)
    assert rs.measurement == measurement


def test_remote_source_constructor_args():
    # noinspection PyArgumentList
    rs = RemoteSource(*remote_source_args)

    verify_remote_point_constructor_args(rs)
    assert rs.measurement == remote_source_args[-1]


def test_auto_two_way_connections_for_remote_source_constructor():
    m = Measurement()
    rs = create_remote_source(measurement=m)

    assert m.remote_source == rs
