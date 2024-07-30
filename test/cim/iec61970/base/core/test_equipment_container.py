#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis.strategies import builds, lists

from cim.collection_validator import validate_collection_unordered
from cim.iec61970.base.core.test_connectivity_node_container import connectivity_node_container_kwargs, \
    verify_connectivity_node_container_constructor_default, verify_connectivity_node_container_constructor_kwargs, \
    verify_connectivity_node_container_constructor_args, connectivity_node_container_args
from zepben.evolve import EquipmentContainer, Equipment, Feeder, LvFeeder, Substation

equipment_container_kwargs = {
    **connectivity_node_container_kwargs,
    "equipment": lists(builds(Equipment), max_size=2)
}

equipment_container_args = [*connectivity_node_container_args, {"e": Equipment()}]


def verify_equipment_container_constructor_default(ec: EquipmentContainer):
    verify_connectivity_node_container_constructor_default(ec)
    assert not list(ec.equipment)


def verify_equipment_container_constructor_kwargs(ec: EquipmentContainer, equipment, **kwargs):
    verify_connectivity_node_container_constructor_kwargs(ec, **kwargs)
    assert list(ec.equipment) == equipment


def verify_equipment_container_constructor_args(ec: EquipmentContainer):
    verify_connectivity_node_container_constructor_args(ec)
    assert list(ec.equipment) == list(equipment_container_args[-1].values())


def test_equipment_collection():
    validate_collection_unordered(EquipmentContainer,
                                  lambda mrid, _: Equipment(mrid),
                                  EquipmentContainer.num_equipment,
                                  EquipmentContainer.get_equipment,
                                  EquipmentContainer.equipment,
                                  EquipmentContainer.add_equipment,
                                  EquipmentContainer.remove_equipment,
                                  EquipmentContainer.clear_equipment,
                                  KeyError)


def test_current_equipment_mirrors_normal_equipment():
    ec = EquipmentContainer()
    eq1 = Equipment(mrid="eq1")
    eq2 = Equipment(mrid="eq2")

    ec.add_equipment(eq1)
    assert ec.get_current_equipment("eq1") == eq1

    ec.add_current_equipment(eq2)
    assert ec.get_equipment("eq2") == eq2


def test_normal_feeders():
    fdr1, fdr2, fdr3 = Feeder(), Feeder(), Feeder()
    substation = Substation()
    lv_fdr = LvFeeder()

    eq1 = Equipment().add_container(fdr1).add_container(fdr2).add_container(substation)
    eq2 = Equipment().add_container(fdr2).add_container(fdr3).add_container(lv_fdr)

    equipment_container = EquipmentContainer().add_equipment(eq1).add_equipment(eq2)

    assert set(equipment_container.normal_feeders()) == {fdr1, fdr2, fdr3}
    assert set(equipment_container.current_feeders()) == set()


def test_current_feeders():
    fdr1, fdr2, fdr3 = Feeder(), Feeder(), Feeder()
    substation = Substation()
    lv_fdr = LvFeeder()

    eq1 = Equipment().add_current_container(fdr1).add_current_container(fdr2).add_current_container(substation)
    eq2 = Equipment().add_current_container(fdr2).add_current_container(fdr3).add_current_container(lv_fdr)

    equipment_container = EquipmentContainer().add_equipment(eq1).add_equipment(eq2)

    assert set(equipment_container.normal_feeders()) == set()
    assert set(equipment_container.current_feeders()) == {fdr1, fdr2, fdr3}


def test_normal_lv_feeders():
    lv_fdr1, lv_fdr2, lv_fdr3 = LvFeeder(), LvFeeder(), LvFeeder()
    substation = Substation()
    fdr = Feeder()

    eq1 = Equipment().add_container(lv_fdr1).add_container(lv_fdr2).add_container(substation)
    eq2 = Equipment().add_container(lv_fdr2).add_container(lv_fdr3).add_container(fdr)

    equipment_container = EquipmentContainer().add_equipment(eq1).add_equipment(eq2)

    assert set(equipment_container.normal_lv_feeders()) == {lv_fdr1, lv_fdr2, lv_fdr3}
    assert set(equipment_container.current_lv_feeders()) == set()


def test_current_lv_feeders():
    lv_fdr1, lv_fdr2, lv_fdr3 = LvFeeder(), LvFeeder(), LvFeeder()
    substation = Substation()
    fdr = Feeder()

    eq1 = Equipment().add_current_container(lv_fdr1).add_current_container(lv_fdr2).add_current_container(substation)
    eq2 = Equipment().add_current_container(lv_fdr2).add_current_container(lv_fdr3).add_current_container(fdr)

    equipment_container = EquipmentContainer().add_equipment(eq1).add_equipment(eq2)

    assert set(equipment_container.normal_lv_feeders()) == set()
    assert set(equipment_container.current_lv_feeders()) == {lv_fdr1, lv_fdr2, lv_fdr3}
