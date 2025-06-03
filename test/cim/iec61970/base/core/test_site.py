#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest
from hypothesis import given

from zepben.evolve.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
from cim.iec61970.base.core.test_equipment_container import equipment_container_kwargs, verify_equipment_container_constructor_default, \
    verify_equipment_container_constructor_kwargs, verify_equipment_container_constructor_args, equipment_container_args
from zepben.evolve import Site, TestNetworkBuilder, Equipment, AssignToLvFeeders, LvFeeder

site_kwargs = equipment_container_kwargs
site_args = equipment_container_args


def test_site_constructor_default():
    verify_equipment_container_constructor_default(Site())


@given(**site_kwargs)
def test_site_constructor_kwargs(**kwargs):
    verify_equipment_container_constructor_kwargs(Site(**kwargs), **kwargs)


def test_site_constructor_args():
    verify_equipment_container_constructor_args(Site(*site_args))

@pytest.mark.asyncio
async def test_find_lv_feeders_excludes_open_switches():
    #
    # tx0 21 b1(lvf5) 21--c2--2
    #     21 b3(lvf6) 21--c4--2
    #
    site = Site()
    network = (TestNetworkBuilder()
               .from_power_transformer(action=lambda pt: _add_to_site(pt, site))  # tx0
               .from_breaker(is_normally_open=True, is_open=True, action=lambda b: _add_to_site(b, site))  # b1
               .to_acls()  # c2
               .branch_from('tx0')
               .to_breaker(is_normally_open=False, is_open=False, action=lambda b: _add_to_site(b, site))  # b3
               .to_acls()  # c4
               .add_lv_feeder('b1')  # lvf5
               .add_lv_feeder('b3')  # lvf6
               ).network

    assign_to_lv_feeders = AssignToLvFeeders()

    await assign_to_lv_feeders.run(network, network_state_operators=NetworkStateOperators.NORMAL, start_terminal=network.get('b1-t2'))
    await assign_to_lv_feeders.run(network, network_state_operators=NetworkStateOperators.NORMAL, start_terminal=network.get('b3-t2'))
    await assign_to_lv_feeders.run(network, network_state_operators=NetworkStateOperators.CURRENT, start_terminal=network.get('b1-t2'))
    await assign_to_lv_feeders.run(network, network_state_operators=NetworkStateOperators.CURRENT, start_terminal=network.get('b3-t2'))

    lvf6 = network.get('lvf6', LvFeeder)
    normal_lv_feeders = list(site.find_lv_feeders(network.lv_feeder_start_points, NetworkStateOperators.NORMAL))
    assert normal_lv_feeders == [lvf6]

    current_lv_feeders = list(site.find_lv_feeders(network.lv_feeder_start_points, NetworkStateOperators.CURRENT))
    assert current_lv_feeders == [lvf6]


def _add_to_site(equipment: Equipment, site: Site):
    site.add_equipment(equipment)
    equipment.add_container(site)
    site.add_current_equipment(equipment)
    equipment.add_current_container(site)
    