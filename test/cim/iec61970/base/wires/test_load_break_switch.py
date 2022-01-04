#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import data

from test.cim.common_testing_functions import verify
from test.cim.test_common_two_way_connections import set_up_conducting_equipment_two_way_link_test, check_conducting_equipment_two_way_link_test
from test.cim.iec61970.base.wires.test_protected_switch import verify_protected_switch_constructor_default, \
    verify_protected_switch_constructor_kwargs, verify_protected_switch_constructor_args, protected_switch_kwargs, protected_switch_args
from zepben.evolve import LoadBreakSwitch
from zepben.evolve.model.cim.iec61970.base.wires.create_wires_components import create_load_break_switch

load_break_switch_kwargs = protected_switch_kwargs
load_break_switch_args = protected_switch_args


def test_load_break_switch_constructor_default():
    verify_protected_switch_constructor_default(LoadBreakSwitch())
    verify_protected_switch_constructor_default(create_load_break_switch())


# noinspection PyShadowingNames
@given(data())
def test_load_breaker_switch_constructor_kwargs(data):
    verify(
        [LoadBreakSwitch, create_load_break_switch],
        data, load_break_switch_kwargs, verify_protected_switch_constructor_kwargs
    )


def test_load_break_switch_constructor_args():
    verify_protected_switch_constructor_args(LoadBreakSwitch(*load_break_switch_args))


def test_auto_two_way_connections_for_load_break_switch_constructor():
    up, ec, opr, f, t = set_up_conducting_equipment_two_way_link_test()
    j = create_load_break_switch(usage_points=[up], equipment_containers=[ec], operational_restrictions=[opr], current_feeders=[f], terminals=[t])
    check_conducting_equipment_two_way_link_test(j, up, ec, opr, f, t)
