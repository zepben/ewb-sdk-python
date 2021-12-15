#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.test_common_two_way_connections import set_up_conducting_equipment_two_way_link_test, check_conducting_equipment_two_way_link_test
from test.cim.iec61970.base.wires.test_switch import verify_switch_constructor_default, verify_switch_constructor_kwargs, verify_switch_constructor_args, \
    switch_kwargs, switch_args
from zepben.evolve import Fuse
from zepben.evolve.model.cim.iec61970.base.wires.create_wires_components import create_fuse

fuse_kwargs = switch_kwargs
fuse_args = switch_args


def test_fuse_constructor_default():
    verify_switch_constructor_default(Fuse())
    verify_switch_constructor_default(create_fuse())


@given(**fuse_kwargs)
def test_fuse_constructor_kwargs(**kwargs):
    verify_switch_constructor_kwargs(Fuse(**kwargs), **kwargs)


@given(**fuse_kwargs)
def test_fuse_creator(**kwargs):
    verify_switch_constructor_kwargs(create_fuse(**kwargs), **kwargs)


def test_fuse_constructor_args():
    verify_switch_constructor_args(Fuse(*fuse_args))


def test_auto_two_way_connections_for_fuse_constructor():
    up, ec, opr, f, t = set_up_conducting_equipment_two_way_link_test()
    fu = create_fuse(usage_points=[up], equipment_containers=[ec], operational_restrictions=[opr], current_feeders=[f], terminals=[t])
    check_conducting_equipment_two_way_link_test(fu, up, ec, opr, f, t)
