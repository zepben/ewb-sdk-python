#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from zepben.evolve.model.cim.iec61970.base.core.equipment_container import EquipmentContainer, Feeder
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.lv_feeder import LvFeeder

from abc import abstractmethod
from typing import Generator, TYPE_CHECKING

from zepben.evolve.services.network.tracing.networktrace.operators import StateOperator

if TYPE_CHECKING:
    from zepben.evolve.model.cim.iec61970.base.core.equipment import Equipment

__all__ = ['EquipmentContainerStateOperators', 'NormalEquipmentContainerStateOperators', 'CurrentEquipmentContainerStateOperators']


class EquipmentContainerStateOperators(StateOperator):
    """
    Defines operations for managing relationships between [Equipment] and [EquipmentContainer].
    """

    @staticmethod
    @abstractmethod
    def get_equipment(container: EquipmentContainer) -> Generator[Equipment, None, None]:
        """
        Get the collection of equipment associated with the given container.

        `container` The container for which to get the associated equipment.
        Returns A collection of equipment in the specified container.
        """
        pass

    @staticmethod
    @abstractmethod
    def get_containers(equipment: Equipment) -> Generator[EquipmentContainer, None, None]:
        """
        Retrieves a collection of containers associated with the given equipment.

        `equipment` The equipment for which to get the associated containers.
        Returns A collection of containers that contain the specified equipment.
        """
        pass

    @staticmethod
    @abstractmethod
    def get_energizing_feeders(lv_feeder:  LvFeeder) -> Generator[Feeder, None, None]:
        """
        Retrieves a collection of feeders that energize the given LV feeder.

        `lvFeeder` The LV feeder for which to get the energizing feeders.
        Returns A collection of feeders that energize the given LV feeder.
        """
        pass

    @staticmethod
    @abstractmethod
    def get_energized_lv_feeders(feeder: Feeder) -> Generator[LvFeeder, None, None]:
        """
        Retrieves a collection of LV feeders energized by the given feeder.

        `feeder` The feeder for which to get the energized LV feeders.
        Returns A collection of LV feeders energized by the given feeder.
        """
        pass

    @staticmethod
    @abstractmethod
    def add_equipment_to_container(equipment: Equipment, container: EquipmentContainer):
        """
         Adds the specified equipment to the given container.

         `equipment` The equipment to add to the container.
         `container` The container to which the equipment will be added.
        """
        pass

    @staticmethod
    @abstractmethod
    def add_container_to_equipment(container: EquipmentContainer, equipment: Equipment):
        """
        Adds the specified container to the given equipment.

        `container` The container to add to the equipment.
        `equipment` The equipment to which the container will be added.
        """
        pass

    @classmethod
    def associate_equipment_and_container(cls, equipment: Equipment, container: EquipmentContainer):
        """
        Establishes a bidirectional association between the specified equipment and container.

        `equipment` The equipment to associate with the container.
        `container` The container to associate with the equipment.
        """
        cls.add_equipment_to_container(equipment, container)
        cls.add_container_to_equipment(container, equipment)

    @staticmethod
    @abstractmethod
    def remove_equipment_from_container(equipment: Equipment, container: EquipmentContainer):
        """
        Removes the specified equipment from the given container.

        `equipment` The equipment to remove from the container.
        `container` The container from which the equipment will be removed.
        """
        pass

    @staticmethod
    @abstractmethod
    def remove_container_from_equipment(container: EquipmentContainer, equipment: Equipment):
        """
        Removes the specified container from the given equipment.

        `container` The container to remove from the equipment.
        `equipment` The equipment from which the container will be removed.
        """
        pass

    @classmethod
    def disassociate_equipment_and_container(cls, equipment: Equipment, container: EquipmentContainer):
        """
        Remove a bidirectional association between the specified equipment and container.

        `equipment` The equipment to disassociate with the container.
        `container` The container to disassociate with the equipment.
        """
        cls.remove_equipment_from_container(equipment, container)
        cls.remove_container_from_equipment(container, equipment)

    @staticmethod
    @abstractmethod
    def add_energizing_feeder_to_lv_feeder(feeder: Feeder, lv_feeder: LvFeeder):
        """
        Adds the specified energizing feeder to the given lvFeeder.

        `feeder` The energizing feeder to add to the lvFeeder.
        `lvFeeder` The lvFeeder to which the feeder will be added.
        """
        pass

    @staticmethod
    @abstractmethod
    def add_energizing_lv_feeder_to_feeder(lv_feeder: LvFeeder, feeder: Feeder):
        """
        Adds the specified energized lvFeeder to the given feeder.

        `lvFeeder` The energized lvFeeder to add to the feeder.
        `feeder` The feeder to which the lvFeeder will be added.
        """
        pass

    @classmethod
    def associate_energizing_feeder(cls, feeder: Feeder, lv_feeder: LvFeeder):
        """
        Establishes a bidirectional association between the specified feeder and LV feeder.

        `feeder` The feeder energizing the lv feeder.
        `lvFeeder` The lv feeder energized by the feeder.
        """
        cls.add_energizing_feeder_to_lv_feeder(feeder, lv_feeder)
        cls.add_energizing_lv_feeder_to_feeder(lv_feeder, feeder)


class NormalEquipmentContainerStateOperators(EquipmentContainerStateOperators):
    """
    Operates on the normal network state equipment-container relationships
    """
    @staticmethod
    def get_equipment(container: EquipmentContainer) -> Generator[Equipment, None, None]:
        return container.equipment

    @staticmethod
    def get_containers(equipment: Equipment) -> Generator[EquipmentContainer, None, None]:
        return equipment.containers

    @staticmethod
    def get_energizing_feeders(lv_feeder:  LvFeeder) -> Generator[Feeder, None, None]:
        return lv_feeder.normal_energizing_feeders

    @staticmethod
    def get_energized_lv_feeders(feeder: Feeder) -> Generator[LvFeeder, None, None]:
        return feeder.normal_energized_lv_feeders

    @staticmethod
    def add_equipment_to_container(equipment: Equipment, container: EquipmentContainer):
        container.add_equipment(equipment)

    @staticmethod
    def add_container_to_equipment(container: EquipmentContainer, equipment: Equipment):
        equipment.add_container(container)

    @staticmethod
    def remove_equipment_from_container(equipment: Equipment, container: EquipmentContainer):
        container.remove_equipment(equipment)

    @staticmethod
    def remove_container_from_equipment(container: EquipmentContainer, equipment: Equipment):
        equipment.remove_container(container)

    @staticmethod
    def add_energizing_feeder_to_lv_feeder(feeder: Feeder, lv_feeder: LvFeeder):
        lv_feeder.add_normal_energizing_feeder(feeder)

    @staticmethod
    def add_energizing_lv_feeder_to_feeder(lv_feeder: LvFeeder, feeder: Feeder):
        feeder.add_normal_energized_lv_feeder(lv_feeder)


class CurrentEquipmentContainerStateOperators(EquipmentContainerStateOperators):
    """
    Operates on the current network state equipment-container relationships
    """
    @staticmethod
    def get_equipment(container: EquipmentContainer) -> Generator[Equipment, None, None]:
        return container.current_equipment

    @staticmethod
    def get_containers(equipment: Equipment) -> Generator[EquipmentContainer, None, None]:
        return equipment.current_containers

    @staticmethod
    def get_energizing_feeders(lv_feeder: LvFeeder) -> Generator[Feeder, None, None]:
        return lv_feeder.current_energizing_feeders

    @staticmethod
    def get_energized_lv_feeders(feeder: Feeder) -> Generator[LvFeeder, None, None]:
        return feeder.current_energized_lv_feeders

    @staticmethod
    def add_equipment_to_container(equipment: Equipment, container: EquipmentContainer):
        container.add_current_equipment(equipment)

    @staticmethod
    def add_container_to_equipment(container: EquipmentContainer, equipment: Equipment):
        equipment.add_current_container(container)

    @staticmethod
    def remove_equipment_from_container(equipment: Equipment, container: EquipmentContainer):
        container.remove_current_equipment(equipment)

    @staticmethod
    def remove_container_from_equipment(container: EquipmentContainer, equipment: Equipment):
        equipment.remove_current_container(container)

    @staticmethod
    def add_energizing_feeder_to_lv_feeder(feeder: Feeder, lv_feeder: LvFeeder):
        lv_feeder.add_current_energizing_feeder(feeder)

    @staticmethod
    def add_energizing_lv_feeder_to_feeder(lv_feeder: LvFeeder, feeder: Feeder):
        feeder.add_current_energized_lv_feeder(lv_feeder)

EquipmentContainerStateOperators.NORMAL = NormalEquipmentContainerStateOperators
EquipmentContainerStateOperators.CURRENT = CurrentEquipmentContainerStateOperators

