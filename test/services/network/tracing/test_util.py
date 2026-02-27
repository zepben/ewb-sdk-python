#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https:#mozilla.org/MPL/2.0/.
import pytest

from zepben.ewb import LvSubstation, generate_id, TestNetworkBuilder, Site, Equipment, EquipmentContainer, Tracing, NetworkStateOperators


@pytest.mark.asyncio
async def test_find_lv_feeders_works_for_sites_and_substations():
    #
    # tx0 21 b1(lvf5) 21--c2--2
    #     21 b3(lvf6) 21--c4--2
    lv_sub = LvSubstation(mrid=generate_id())
    site = Site(mrid=generate_id())
    network = (TestNetworkBuilder()
               .from_power_transformer(action=lambda it: _add_equipment_to_site(it, site))  # tx0
               .to_breaker(is_normally_open=True, is_open=True, action=lambda it: _add_equipment_to_site(it, site))  # b1
               .to_acls()  # c2
               .branch_from("tx0")
               .to_breaker(is_normally_open=False, is_open=False, action=lambda it: _add_equipment_to_site(it, site))  # b3
               .to_acls()  # c4
               .add_lv_feeder("b1")  # lvf5
               .add_lv_feeder("b3")  # lvf6
               ).network
    assign_to_lv_feeders = Tracing.assign_equipment_to_lv_feeders()

    await assign_to_lv_feeders.run(network, NetworkStateOperators.NORMAL, network.get("b1")[2])
    await assign_to_lv_feeders.run(network, NetworkStateOperators.NORMAL, network.get("b3")[2])
    await assign_to_lv_feeders.run(network, NetworkStateOperators.CURRENT, network.get("b1")[2])
    await assign_to_lv_feeders.run(network, NetworkStateOperators.CURRENT, network.get("b3")[2])

    lvf6 = network.get("lvf6")
    normal_lv_feeders = list(site.find_lv_feeders(network.lv_feeder_start_points, NetworkStateOperators.NORMAL))
    assert normal_lv_feeders == [lvf6]

    current_lv_feeders = list(site.find_lv_feeders(network.lv_feeder_start_points, NetworkStateOperators.CURRENT))
    assert current_lv_feeders == [lvf6]


@pytest.mark.asyncio
async def test_find_lv_feeders_works_for_sites_and_substations():
    #
    # tx0 21 b1(lvf5) 21--c2--2
    #     21 b3(lvf6) 21--c4--2
    lvSub = LvSubstation(mrid=generate_id())
    site = Site(mrid=generate_id())
    network = (TestNetworkBuilder()
        .from_power_transformer(action=lambda it: _add_equipment_to_site(it, site) and _add_equipment_to_site(it, lvSub))
        .to_breaker(is_normally_open=True, is_open=True, action=lambda it: _add_equipment_to_site(it, site) and _add_equipment_to_site(it, lvSub))
        .to_acls() # c2
        .branch_from("tx0")
        .to_breaker(is_normally_open=False, is_open=False, action=lambda it: _add_equipment_to_site(it, site) and _add_equipment_to_site(it, lvSub))
        .to_acls() # c4
        .add_lv_feeder("b1") # lvf5
        .add_lv_feeder("b3") # lvf6
    ).network
    assign_to_lv_feeders = Tracing.assign_equipment_to_lv_feeders()

    await assign_to_lv_feeders.run(network, NetworkStateOperators.NORMAL, network.get("b1")[2])
    await assign_to_lv_feeders.run(network, NetworkStateOperators.NORMAL, network.get("b3")[2])
    await assign_to_lv_feeders.run(network, NetworkStateOperators.CURRENT, network.get("b1")[2])
    await assign_to_lv_feeders.run(network, NetworkStateOperators.CURRENT, network.get("b3")[2])

    lvf6 = network.get("lvf6")
    normal_lv_feeders = list(site.find_lv_feeders(network.lv_feeder_start_points, NetworkStateOperators.NORMAL))
    assert normal_lv_feeders == [lvf6]

    current_lv_feeders = list(site.find_lv_feeders(network.lv_feeder_start_points, NetworkStateOperators.CURRENT))
    assert current_lv_feeders == [lvf6]


def _add_equipment_to_site(equipment: Equipment, site: EquipmentContainer):
    site.add_equipment(equipment)
    equipment.add_container(site)
    site.add_current_equipment(equipment)
    equipment.add_current_container(site)