#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from cim.fill_fields import remote_source_kwargs
from cim.iec61970.base.scada.test_remote_point import verify_remote_point_constructor_default, \
    verify_remote_point_constructor_kwargs, remote_point_args
from hypothesis import given

from zepben.ewb import RemoteSource, Measurement, generate_id

remote_source_args = [*remote_point_args, Measurement(mrid=generate_id())]


def test_remote_source_constructor_default():
    c = RemoteSource(mrid=generate_id())

    verify_remote_point_constructor_default(c)
    assert not c.measurement


@given(**remote_source_kwargs())
def test_remote_source_constructor_kwargs(measurement, **kwargs):
    c = RemoteSource(measurement=measurement, **kwargs)

    verify_remote_point_constructor_kwargs(c, **kwargs)
    assert c.measurement == measurement
