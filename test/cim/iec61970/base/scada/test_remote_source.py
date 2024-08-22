#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds
from zepben.evolve import RemoteSource, Measurement

from cim.iec61970.base.scada.test_remote_point import remote_point_kwargs, verify_remote_point_constructor_default, \
    verify_remote_point_constructor_kwargs, verify_remote_point_constructor_args, remote_point_args

remote_source_kwargs = {
    **remote_point_kwargs,
    "measurement": builds(Measurement)
}

remote_source_args = [*remote_point_args, Measurement()]


def test_remote_source_constructor_default():
    c = RemoteSource()

    verify_remote_point_constructor_default(c)
    assert not c.measurement


@given(**remote_source_kwargs)
def test_remote_source_constructor_kwargs(measurement, **kwargs):
    c = RemoteSource(measurement=measurement, **kwargs)

    verify_remote_point_constructor_kwargs(c, **kwargs)
    assert c.measurement == measurement


def test_remote_source_constructor_args():
    c = RemoteSource(*remote_source_args)

    verify_remote_point_constructor_args(c)
    assert remote_source_args[-1:] == [
        c.measurement
    ]
