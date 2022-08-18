#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis.strategies import builds, lists

from cim.collection_validator import validate_collection_unordered
from cim.iec61970.base.core.test_connectivity_node_container import connectivity_node_container_kwargs, \
    verify_connectivity_node_container_constructor_default, verify_connectivity_node_container_constructor_kwargs, \
    verify_connectivity_node_container_constructor_args, connectivity_node_container_args
from zepben.evolve import EquipmentContainer, Equipment

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
