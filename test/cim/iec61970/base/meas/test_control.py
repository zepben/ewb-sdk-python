#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, text

from cim.iec61970.base.meas.test_io_point import io_point_kwargs, verify_io_point_constructor_default, \
    verify_io_point_constructor_kwargs, verify_io_point_constructor_args, io_point_args
from cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE
from zepben.evolve import Control, RemoteControl

control_kwargs = {
    **io_point_kwargs,
    "power_system_resource_mrid": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "remote_control": builds(RemoteControl)
}

control_args = [*io_point_args, "a", RemoteControl()]


def test_control_constructor_default():
    c = Control()

    verify_io_point_constructor_default(c)
    assert not c.power_system_resource_mrid
    assert not c.remote_control


@given(**control_kwargs)
def test_control_constructor_kwargs(power_system_resource_mrid, remote_control, **kwargs):
    # noinspection PyArgumentList
    c = Control(power_system_resource_mrid=power_system_resource_mrid, remote_control=remote_control, **kwargs)

    verify_io_point_constructor_kwargs(c, **kwargs)
    assert c.power_system_resource_mrid == power_system_resource_mrid
    assert c.remote_control == remote_control


def test_control_constructor_args():
    # noinspection PyArgumentList
    c = Control(*control_args)

    verify_io_point_constructor_args(c)
    assert c.power_system_resource_mrid == control_args[-2]
    assert c.remote_control == control_args[-1]
