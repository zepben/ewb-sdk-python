#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds

from cim.iec61970.base.scada.test_remote_point import remote_point_kwargs, verify_remote_point_constructor_default, \
    verify_remote_point_constructor_kwargs, verify_remote_point_constructor_args, remote_point_args
from zepben.evolve import RemoteControl, Control

remote_control_kwargs = {
    **remote_point_kwargs,
    "control": builds(Control)
}

remote_control_args = [*remote_point_args, Control()]


def test_remote_control_constructor_default():
    rc = RemoteControl()

    verify_remote_point_constructor_default(rc)
    assert not rc.control


@given(**remote_control_kwargs)
def test_remote_control_constructor_kwargs(control, **kwargs):
    # noinspection PyArgumentList
    rc = RemoteControl(control=control, **kwargs)

    verify_remote_point_constructor_kwargs(rc, **kwargs)
    assert rc.control == control


def test_remote_control_constructor_args():
    # noinspection PyArgumentList
    c = RemoteControl(*remote_control_args)

    verify_remote_point_constructor_args(c)
    assert c.control == remote_control_args[-1]
