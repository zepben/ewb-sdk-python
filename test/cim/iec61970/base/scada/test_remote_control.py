#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from cim.fill_fields import remote_control_kwargs
from cim.iec61970.base.scada.test_remote_point import verify_remote_point_constructor_default, \
    verify_remote_point_constructor_kwargs, remote_point_args
from hypothesis import given

from zepben.ewb import RemoteControl, Control, generate_id

remote_control_args = [*remote_point_args, Control(mrid=generate_id())]


def test_remote_control_constructor_default():
    rc = RemoteControl(mrid=generate_id())

    verify_remote_point_constructor_default(rc)
    assert not rc.control


@given(**remote_control_kwargs())
def test_remote_control_constructor_kwargs(control, **kwargs):
    # noinspection PyArgumentList
    rc = RemoteControl(control=control, **kwargs)

    verify_remote_point_constructor_kwargs(rc, **kwargs)
    assert rc.control == control
