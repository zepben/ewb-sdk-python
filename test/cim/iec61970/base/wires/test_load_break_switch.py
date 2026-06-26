#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.fill_fields import load_break_switch_kwargs
from cim.iec61970.base.wires.test_protected_switch import verify_protected_switch_constructor_default, \
    verify_protected_switch_constructor_kwargs
from zepben.ewb import LoadBreakSwitch, generate_id


def test_load_break_switch_constructor_default():
    verify_protected_switch_constructor_default(LoadBreakSwitch(mrid=generate_id()))


@given(**load_break_switch_kwargs())
def test_load_break_switch_constructor_kwargs(**kwargs):
    verify_protected_switch_constructor_kwargs(LoadBreakSwitch(**kwargs), **kwargs)
