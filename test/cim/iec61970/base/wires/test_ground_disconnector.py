#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.iec61970.base.wires.test_switch import verify_switch_constructor_default, verify_switch_constructor_kwargs, verify_switch_constructor_args, \
    switch_kwargs, switch_args
from zepben.evolve import GroundDisconnector

ground_disconnector_kwargs = switch_kwargs
ground_disconnector_args = switch_args


def test_ground_disconnector_constructor_default():
    verify_switch_constructor_default(GroundDisconnector())


@given(**ground_disconnector_kwargs)
def test_ground_disconnector_constructor_kwargs(**kwargs):
    verify_switch_constructor_kwargs(GroundDisconnector(**kwargs), **kwargs)


def test_ground_disconnector_constructor_args():
    verify_switch_constructor_args(GroundDisconnector(*ground_disconnector_args))
