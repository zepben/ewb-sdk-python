#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from test.cim.test_common_two_way_connections import set_up_conducting_equipment_two_way_link_test, check_conducting_equipment_two_way_link_test
from test.cim.iec61970.base.wires.test_protected_switch import verify_protected_switch_constructor_default, \
    verify_protected_switch_constructor_kwargs, verify_protected_switch_constructor_args, protected_switch_kwargs, protected_switch_args
from zepben.evolve import Breaker
from zepben.evolve.model.cim.iec61970.base.wires.create_wires_components import create_breaker

breaker_kwargs = protected_switch_kwargs
breaker_args = protected_switch_args


def test_breaker_constructor_default():
    verify_protected_switch_constructor_default(Breaker())
    verify_protected_switch_constructor_default(create_breaker())


@given(**breaker_kwargs)
def test_breaker_constructor_kwargs(**kwargs):
    verify_protected_switch_constructor_kwargs(Breaker(**kwargs), **kwargs)


@given(**breaker_kwargs)
def test_breaker_creator(**kwargs):
    verify_protected_switch_constructor_kwargs(create_breaker(**kwargs), **kwargs)


def test_breaker_constructor_args():
    verify_protected_switch_constructor_args(Breaker(*breaker_args))


def test_auto_two_way_connections_for_breaker_constructor():
    up, ec, opr, f, t = set_up_conducting_equipment_two_way_link_test()
    b = create_breaker(usage_points=[up], equipment_containers=[ec], operational_restrictions=[opr], current_feeders=[f], terminals=[t])
    check_conducting_equipment_two_way_link_test(b, up, ec, opr, f, t)
