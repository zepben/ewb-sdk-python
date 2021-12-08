#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds

from cim import extract_testing_args
from test.cim.iec61970.base.scada.test_remote_point import remote_point_kwargs, verify_remote_point_constructor_default, \
    verify_remote_point_constructor_kwargs, verify_remote_point_constructor_args, remote_point_args
from zepben.evolve import RemoteControl, Control
from zepben.evolve.model.cim.iec61970.base.scada.create_scada_components import create_remote_control

remote_control_kwargs = {
    **remote_point_kwargs,
    "control": builds(Control)
}

remote_control_args = [*remote_point_args, Control()]


def test_remote_control_constructor_default():
    rc = RemoteControl()
    rc2 = create_remote_control()
    validate_default_remote_control_constructor(rc)
    validate_default_remote_control_constructor(rc2)


def validate_default_remote_control_constructor(rc):
    verify_remote_point_constructor_default(rc)
    assert not rc.control


@given(**remote_control_kwargs)
def test_remote_control_constructor_kwargs(control, **kwargs):
    args = extract_testing_args(locals())
    rc = RemoteControl(**args, **kwargs)
    validate_remote_control_values(rc, **args, **kwargs)


@given(**remote_control_kwargs)
def test_remote_control_creator(control, **kwargs):
    args = extract_testing_args(locals())
    rc = create_remote_control(**args, **kwargs)
    validate_remote_control_values(rc, **args, **kwargs)


def validate_remote_control_values(rc, control, **kwargs):
    verify_remote_point_constructor_kwargs(rc, **kwargs)
    assert rc.control == control


def test_remote_control_constructor_args():
    # noinspection PyArgumentList
    c = RemoteControl(*remote_control_args)

    verify_remote_point_constructor_args(c)
    assert c.control == remote_control_args[-1]
