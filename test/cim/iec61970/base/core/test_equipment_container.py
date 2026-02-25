#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Generator, Type

import pytest

from hypothesis.strategies import builds, lists

from cim.iec61970.base.core.test_connectivity_node_container import connectivity_node_container_kwargs, \
    verify_connectivity_node_container_constructor_default, verify_connectivity_node_container_constructor_kwargs, \
    verify_connectivity_node_container_constructor_args, connectivity_node_container_args
from cim.private_collection_validator import validate_unordered
from util import mrid_strategy
from zepben.ewb import EquipmentContainer, Equipment, LvFeeder, Substation, generate_id, TestNetworkBuilder, NetworkStateOperators
from zepben.ewb.model.cim.iec61970.base.core.feeder import Feeder

equipment_container_kwargs = {
    **connectivity_node_container_kwargs,
    "equipment": lists(builds(Equipment, mrid=mrid_strategy), max_size=2)
}

equipment_container_args = [*connectivity_node_container_args, {"e": Equipment(mrid=generate_id())}]


def verify_equipment_container_constructor_default(ec: EquipmentContainer):
    verify_connectivity_node_container_constructor_default(ec)
    assert not list(ec.equipment)


def verify_equipment_container_constructor_kwargs(ec: EquipmentContainer, equipment, **kwargs):
    verify_connectivity_node_container_constructor_kwargs(ec, **kwargs)
    assert list(ec.equipment) == equipment


def verify_equipment_container_constructor_args(ec: EquipmentContainer):
    verify_connectivity_node_container_constructor_args(ec)

    # We use a different style of matching here as the passed in arg for equipment is a map and the stored collection is a list.
    assert list(ec.equipment) == list(equipment_container_args[-1].values())


def test_equipment_collection():
    validate_unordered(
        EquipmentContainer,
        lambda mrid: Equipment(mrid),
        EquipmentContainer.equipment,
        EquipmentContainer.num_equipment,
        EquipmentContainer.get_equipment,
        EquipmentContainer.add_equipment,
        EquipmentContainer.remove_equipment,
        EquipmentContainer.clear_equipment
    )


def test_current_equipment_mirrors_normal_equipment():
    ec = EquipmentContainer(mrid=generate_id())
    eq1 = Equipment(mrid="eq1")
    eq2 = Equipment(mrid="eq2")

    ec.add_equipment(eq1)
    assert ec.get_current_equipment("eq1") == eq1

    ec.add_current_equipment(eq2)
    assert ec.get_equipment("eq2") == eq2


def test_normal_feeders():
    fdr1, fdr2, fdr3 = Feeder(mrid=generate_id()), Feeder(mrid=generate_id()), Feeder(mrid=generate_id())
    substation = Substation(mrid=generate_id())
    lv_fdr = LvFeeder(mrid=generate_id())

    eq1 = Equipment(mrid=generate_id()).add_container(fdr1).add_container(fdr2).add_container(substation)
    eq2 = Equipment(mrid=generate_id()).add_container(fdr2).add_container(fdr3).add_container(lv_fdr)

    equipment_container = EquipmentContainer(mrid=generate_id()).add_equipment(eq1).add_equipment(eq2)

    assert set(equipment_container.normal_feeders()) == {fdr1, fdr2, fdr3}
    assert set(equipment_container.current_feeders()) == set()


def test_current_feeders():
    fdr1, fdr2, fdr3 = Feeder(mrid=generate_id()), Feeder(mrid=generate_id()), Feeder(mrid=generate_id())
    substation = Substation(mrid=generate_id())
    lv_fdr = LvFeeder(mrid=generate_id())

    eq1 = Equipment(mrid=generate_id()).add_current_container(fdr1).add_current_container(fdr2).add_current_container(substation)
    eq2 = Equipment(mrid=generate_id()).add_current_container(fdr2).add_current_container(fdr3).add_current_container(lv_fdr)

    equipment_container = EquipmentContainer(mrid=generate_id()).add_equipment(eq1).add_equipment(eq2)

    assert set(equipment_container.normal_feeders()) == set()
    assert set(equipment_container.current_feeders()) == {fdr1, fdr2, fdr3}


def test_normal_lv_feeders():
    lv_fdr1, lv_fdr2, lv_fdr3 = LvFeeder(mrid=generate_id()), LvFeeder(mrid=generate_id()), LvFeeder(mrid=generate_id())
    substation = Substation(mrid=generate_id())
    fdr = Feeder(mrid=generate_id())

    eq1 = Equipment(mrid=generate_id()).add_container(lv_fdr1).add_container(lv_fdr2).add_container(substation)
    eq2 = Equipment(mrid=generate_id()).add_container(lv_fdr2).add_container(lv_fdr3).add_container(fdr)

    equipment_container = EquipmentContainer(mrid=generate_id()).add_equipment(eq1).add_equipment(eq2)

    assert set(equipment_container.normal_lv_feeders()) == {lv_fdr1, lv_fdr2, lv_fdr3}
    assert set(equipment_container.current_lv_feeders()) == set()


def test_current_lv_feeders():
    lv_fdr1, lv_fdr2, lv_fdr3 = LvFeeder(mrid=generate_id()), LvFeeder(mrid=generate_id()), LvFeeder(mrid=generate_id())
    substation = Substation(mrid=generate_id())
    fdr = Feeder(mrid=generate_id())

    eq1 = Equipment(mrid=generate_id()).add_current_container(lv_fdr1).add_current_container(lv_fdr2).add_current_container(substation)
    eq2 = Equipment(mrid=generate_id()).add_current_container(lv_fdr2).add_current_container(lv_fdr3).add_current_container(fdr)

    equipment_container = EquipmentContainer(mrid=generate_id()).add_equipment(eq1).add_equipment(eq2)

    assert set(equipment_container.normal_lv_feeders()) == set()
    assert set(equipment_container.current_lv_feeders()) == {lv_fdr1, lv_fdr2, lv_fdr3}


@pytest.mark.asyncio
async def test_detects_edge_terminals_correctly():
    network = await (
        TestNetworkBuilder()
        .from_power_transformer()   # tx0
        .to_busbar_section()        # bbs1
        .to_breaker()               # b2  edge of substation, feeder
        .to_acls()                  # c3
        .to_power_transformer()     # tx4 edge of feeder, lv substation, tx4 lv feeder
        .to_busbar_section()        # bbs5
        .to_breaker()               # b6  edge of lv substation, tx4 lv feeder, b6 lv feeder
        .to_acls()                  # c7
        .to_energy_consumer()       # ec8
        .branch_from("tx0")
        .to_breaker()               # b9 edge of substation
        .to_acls()                  # c10
        .add_feeder("b2")           # fdr11
        .add_lv_feeder("tx4")       # lvf12
        .add_lv_feeder("b6")        # lvf13
        .add_lv_substation(["tx4", "bbs5", "b6"])  # lvs14
        .add_substation(["tx0", "bbs1", "b2", "b9"])  # sub15
        .build()
    )

    feeder = network['fdr11']
    lvf_tx = network['lvf12']
    lvf_b = network['lvf13']
    lv_sub = network['lvs14']
    sub = network['sub15']

    assert list(edge_equip_mrids(feeder)) == ["b2"]
    assert list(edge_equip_mrids(lvf_tx)) == ["tx4", "b6"]
    assert list(edge_equip_mrids(lvf_b)) == ["b6"]
    assert list(edge_equip_mrids(lv_sub)) == ["tx4", "b6"]
    assert list(edge_equip_mrids(sub)) == ["b2", "b9"]

    assert list(edge_equip_mrids(feeder, NetworkStateOperators.CURRENT)) == ["b2"]
    assert list(edge_equip_mrids(lvf_tx, NetworkStateOperators.CURRENT)) == ["tx4", "b6"]
    assert list(edge_equip_mrids(lvf_b, NetworkStateOperators.CURRENT)) == ["b6"]
    assert list(edge_equip_mrids(lv_sub, NetworkStateOperators.CURRENT)) == ["tx4", "b6"]
    assert list(edge_equip_mrids(sub, NetworkStateOperators.CURRENT)) == ["b2", "b9"]


@pytest.mark.asyncio
async def test_detects_edge_terminals_for_open_switch():
    network = await (TestNetworkBuilder()
        .from_power_transformer()
        .to_busbar_section()
        .to_breaker()
        .to_acls()
        .branch_from("tx0", 1)
        .to_acls()
        .to_breaker(is_normally_open=True, is_open=True)
        .to_acls()
        .branch_from("bbs1")
        .to_acls()
        .to_breaker()
        .to_acls()
        .add_substation(["tx0", "bbs1", "b2", "c4", "b5", "c7"])
        .build()
    )

    sub = network['sub10']

    assert list(edge_equip_mrids(sub)) == ['b2', 'b5', 'c7']
    assert list(edge_equip_mrids(sub, NetworkStateOperators.CURRENT)) == ['b2', 'b5', 'c7']

def edge_equip_mrids(ec: EquipmentContainer, state_operators: Type[NetworkStateOperators] = NetworkStateOperators.NORMAL) -> Generator[str, None, None]:
    print("\n\nedge_terminals", list(ec.edge_terminals(state_operators)))
    for t in ec.edge_terminals(state_operators):
        if (it := t.conducting_equipment) is not None:
            yield it.mrid