#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import data

from cim.common_testing_functions import verify
from test.cim.test_common_two_way_connections import set_up_conducting_equipment_two_way_link_test, check_conducting_equipment_two_way_link_test
from test.cim.iec61970.base.wires.test_switch import verify_switch_constructor_default, verify_switch_constructor_kwargs, verify_switch_constructor_args, \
    switch_kwargs, switch_args
from zepben.evolve import Disconnector
from zepben.evolve.model.cim.iec61970.base.wires.create_wires_components import create_disconnector

disconnector_kwargs = switch_kwargs
disconnector_args = switch_args


def test_disconnector_constructor_default():
    verify_switch_constructor_default(Disconnector())
    verify_switch_constructor_default(create_disconnector())


# noinspection PyShadowingNames
@given(data())
def test_disconnector_constructor_kwargs(data):
    verify(
        [Disconnector, create_disconnector],
        data, disconnector_kwargs, verify_switch_constructor_kwargs
    )


def test_disconnector_constructor_args():
    verify_switch_constructor_args(Disconnector(*disconnector_args))


def test_auto_two_way_connections_for_disconnector_constructor():
    up, ec, opr, f, t = set_up_conducting_equipment_two_way_link_test()
    d = create_disconnector(usage_points=[up], equipment_containers=[ec], operational_restrictions=[opr], current_feeders=[f], terminals=[t])
    check_conducting_equipment_two_way_link_test(d, up, ec, opr, f, t)
