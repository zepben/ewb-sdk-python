#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, text

from test.cim import extract_testing_args
from test.cim.iec61970.base.meas.test_io_point import io_point_kwargs, verify_io_point_constructor_default, \
    verify_io_point_constructor_kwargs, verify_io_point_constructor_args, io_point_args
from test.cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE
from zepben.evolve import Control, RemoteControl
from zepben.evolve.model.cim.iec61970.base.meas.create_meas_components import create_control

control_kwargs = {
    **io_point_kwargs,
    "power_system_resource_mrid": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "remote_control": builds(RemoteControl)
}

control_args = [*io_point_args, "a", RemoteControl()]


def test_control_constructor_default():
    c = Control()
    c2 = create_control()
    validate_default_control_constructor(c)
    validate_default_control_constructor(c2)


def validate_default_control_constructor(c):
    verify_io_point_constructor_default(c)
    assert not c.power_system_resource_mrid
    assert not c.remote_control


@given(**control_kwargs)
def test_control_constructor_kwargs(power_system_resource_mrid, remote_control, **kwargs):
    args = extract_testing_args(locals())
    c = Control(**args, **kwargs)
    validate_control_values(c, **args, **kwargs)


@given(**control_kwargs)
def test_control_creator(power_system_resource_mrid, remote_control, **kwargs):
    args = extract_testing_args(locals())
    c = create_control(**args, **kwargs)
    validate_control_values(c, **args, **kwargs)


def validate_control_values(c, power_system_resource_mrid, remote_control, **kwargs):
    verify_io_point_constructor_kwargs(c, **kwargs)
    assert c.power_system_resource_mrid == power_system_resource_mrid
    assert c.remote_control == remote_control


def test_control_constructor_args():
    # noinspection PyArgumentList
    c = Control(*control_args)

    verify_io_point_constructor_args(c)
    assert c.power_system_resource_mrid == control_args[-2]
    assert c.remote_control == control_args[-1]
