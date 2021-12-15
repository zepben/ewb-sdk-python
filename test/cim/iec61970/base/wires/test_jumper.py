#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.test_common_two_way_connections import set_up_conducting_equipment_two_way_link_test, check_conducting_equipment_two_way_link_test
from test.cim.iec61970.base.wires.test_switch import verify_switch_constructor_default, verify_switch_constructor_kwargs, verify_switch_constructor_args, \
    switch_kwargs, switch_args
from zepben.evolve import Jumper
from zepben.evolve.model.cim.iec61970.base.wires.create_wires_components import create_jumper

jumper_kwargs = switch_kwargs
jumper_args = switch_args


def test_jumper_constructor_default():
    verify_switch_constructor_default(Jumper())
    verify_switch_constructor_default(create_jumper())


@given(**jumper_kwargs)
def test_jumper_constructor_kwargs(**kwargs):
    verify_switch_constructor_kwargs(Jumper(**kwargs), **kwargs)


@given(**jumper_kwargs)
def test_jumper_creator(**kwargs):
    verify_switch_constructor_kwargs(create_jumper(**kwargs), **kwargs)


def test_jumper_constructor_args():
    verify_switch_constructor_args(Jumper(*jumper_args))


def test_auto_two_way_connections_for_jumper_constructor():
    up, ec, opr, f, t = set_up_conducting_equipment_two_way_link_test()
    j = create_jumper(usage_points=[up], equipment_containers=[ec], operational_restrictions=[opr], current_feeders=[f], terminals=[t])
    check_conducting_equipment_two_way_link_test(j, up, ec, opr, f, t)
