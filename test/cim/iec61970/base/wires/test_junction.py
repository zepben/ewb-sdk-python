#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import data

from cim.common_testing_functions import verify
from test.cim.test_common_two_way_connections import set_up_conducting_equipment_two_way_link_test, check_conducting_equipment_two_way_link_test
from test.cim.iec61970.base.wires.test_connector import verify_connector_constructor_default, \
    verify_connector_constructor_kwargs, verify_connector_constructor_args, connector_kwargs, connector_args
from zepben.evolve import Junction
from zepben.evolve.model.cim.iec61970.base.wires.create_wires_components import create_junction

junction_kwargs = connector_kwargs
junction_args = connector_args


def test_junction_constructor_default():
    verify_connector_constructor_default(Junction())
    verify_connector_constructor_default(create_junction())


# noinspection PyShadowingNames
@given(data())
def test_junction_constructor_kwargs(data):
    verify(
        [Junction, create_junction],
        data, junction_kwargs, verify_connector_constructor_kwargs
    )


def test_junction_constructor_args():
    verify_connector_constructor_args(Junction(*junction_args))


def test_auto_two_way_connections_for_junction_constructor():
    up, ec, opr, f, t = set_up_conducting_equipment_two_way_link_test()
    j = create_junction(usage_points=[up], equipment_containers=[ec], operational_restrictions=[opr], current_feeders=[f], terminals=[t])
    check_conducting_equipment_two_way_link_test(j, up, ec, opr, f, t)
