#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.iec61970.base.wires.test_switch import verify_switch_constructor_default, verify_switch_constructor_kwargs, verify_switch_constructor_args, \
    switch_kwargs, switch_args
from zepben.evolve import Disconnector

disconnector_kwargs = switch_kwargs
disconnector_args = switch_args


def test_disconnector_constructor_default():
    verify_switch_constructor_default(Disconnector())


@given(**disconnector_kwargs)
def test_disconnector_constructor_kwargs(**kwargs):
    verify_switch_constructor_kwargs(Disconnector(**kwargs), **kwargs)


def test_disconnector_constructor_args():
    verify_switch_constructor_args(Disconnector(*disconnector_args))
