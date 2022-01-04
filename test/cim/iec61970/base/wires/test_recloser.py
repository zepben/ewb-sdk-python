#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import data

from cim.common_testing_functions import verify
from test.cim.test_common_two_way_connections import set_up_conducting_equipment_two_way_link_test, check_conducting_equipment_two_way_link_test
from test.cim.iec61970.base.wires.test_protected_switch import verify_protected_switch_constructor_default, \
    verify_protected_switch_constructor_kwargs, verify_protected_switch_constructor_args, protected_switch_kwargs, protected_switch_args
from zepben.evolve import Recloser
from zepben.evolve.model.cim.iec61970.base.wires.create_wires_components import create_recloser

recloser_kwargs = protected_switch_kwargs
recloser_args = protected_switch_args


def test_recloser_constructor_default():
    verify_protected_switch_constructor_default(Recloser())
    verify_protected_switch_constructor_default(create_recloser())


# noinspection PyShadowingNames
@given(data())
def test_recloser_constructor_kwargs(data):
    verify(
        [Recloser, create_recloser],
        data, recloser_kwargs, verify_protected_switch_constructor_kwargs
    )


def test_recloser_constructor_args():
    verify_protected_switch_constructor_args(Recloser(*recloser_args))


def test_auto_two_way_recloser_constructor():
    up, ec, opr, f, t = set_up_conducting_equipment_two_way_link_test()
    r = create_recloser(usage_points=[up], equipment_containers=[ec], operational_restrictions=[opr], current_feeders=[f], terminals=[t])
    check_conducting_equipment_two_way_link_test(r, up, ec, opr, f, t)
