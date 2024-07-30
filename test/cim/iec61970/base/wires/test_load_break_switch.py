#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.iec61970.base.wires.test_protected_switch import verify_protected_switch_constructor_default, \
    verify_protected_switch_constructor_kwargs, verify_protected_switch_constructor_args, protected_switch_kwargs, protected_switch_args
from zepben.evolve import LoadBreakSwitch

load_break_switch_kwargs = protected_switch_kwargs
load_break_switch_args = protected_switch_args


def test_load_break_switch_constructor_default():
    verify_protected_switch_constructor_default(LoadBreakSwitch())


@given(**load_break_switch_kwargs)
def test_load_break_switch_constructor_kwargs(**kwargs):
    verify_protected_switch_constructor_kwargs(LoadBreakSwitch(**kwargs), **kwargs)


def test_load_break_switch_constructor_args():
    verify_protected_switch_constructor_args(LoadBreakSwitch(*load_break_switch_args))
