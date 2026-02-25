#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ['EquipmentContainerStateOperators', 'NormalEquipmentContainerStateOperators', 'CurrentEquipmentContainerStateOperators']

from abc import abstractmethod
from functools import singledispatchmethod
from typing import Generator, TYPE_CHECKING, overload

from zepben.ewb.model.cim.extensions.iec61970.base.feeder import lv_substation
from zepben.ewb.model.cim.extensions.iec61970.base.feeder.lv_feeder import LvFeeder
from zepben.ewb.model.cim.extensions.iec61970.base.feeder.lv_substation import LvSubstation
from zepben.ewb.model.cim.iec61970.base.core.equipment_container import EquipmentContainer
from zepben.ewb.model.cim.iec61970.base.core.feeder import Feeder
from zepben.ewb.services.network.tracing.networktrace.operators import StateOperator

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.equipment import Equipment


class EquipmentContainerStateOperators(StateOperator):
    """
    Defines operations for managing relationships between [Equipment] and [EquipmentContainer].
    """

    @staticmethod
    @abstractmethod
    def get_equipment(container: EquipmentContainer) -> Generator[Equipment, None, None]:
        """
        Get the collection of equipment associated with the given container.

        :param container: The container for which to get the associated equipment.
        :returns: A collection of equipment in the specified container.
        """

    @staticmethod
    @abstractmethod
    def get_containers(equipment: Equipment) -> Generator[EquipmentContainer, None, None]:
        """
        Retrieves a collection of containers associated with the given equipment.

        :param equipment: The equipment for which to get the associated containers.
        :returns: A collection of containers that contain the specified equipment.
        """

    @staticmethod
    @abstractmethod
    @overload
    def get_energizing_feeders(lv_feeder: LvFeeder) -> Generator[Feeder, None, None]:
        """
        Retrieves a collection of feeders that energize the given LV feeder.

        :param lv_feeder: The LV feeder for which to get the energizing feeders.
        :returns: A collection of feeders that energize the given LV feeder.
        """

    @staticmethod
    @abstractmethod
    @overload
    def get_energizing_feeders(lv_substation: LvSubstation) -> Generator[Feeder, None, None]:
        """
        Retrieves a collection of feeders that energize the given ``LvSubstation``.

        :param lv_substation: The ``LvSubstation ``for which to get the energizing feeders.
        :returns: A collection of feeders that energize the given ``LvSubstation``.
        """

    @staticmethod
    @abstractmethod
    def get_energizing_lv_substation(lv_feeder: LvFeeder) -> LvSubstation | None:
        """  # TODO: jvmsdk docs are wrong
        Retrieves the energizing ``LvSubstation`` that energizes the given ``LvFeeder``.

        :param lv_feeder: The Lv Feeder for which to get the energizing ``LvSubstation``.
        :returns: The ``LvSubstation`` that energizes the given ``LvFeeder``.
        """

    @staticmethod
    @abstractmethod
    @overload
    def get_energized_lv_feeders(feeder: Feeder) -> Generator[LvFeeder, None, None]:
        """
        Retrieves a collection of LV feeders energized by the given feeder.

        :param feeder: The feeder for which to get the energized LV feeders.
        :returns: A collection of LV feeders energized by the given feeder.
        """

    @staticmethod
    @abstractmethod
    @overload
    def get_energized_lv_feeders(lv_substation: LvSubstation) -> Generator[LvFeeder, None, None]:
        """
        Retrieves a collection of LV feeders energized by the given ``LvSubstation``.

        :param lv_substation: The ``LvSubstation`` for which to get the energized LV feeders.
        :returns: A collection of LV feeders energized by the given ``LvSubstation``.
        """

    @staticmethod
    @abstractmethod
    def get_energized_lv_substations(feeder: Feeder) -> Generator[LvSubstation, None, None]:
        """
        Retrieves a collection of ``LvSubstation``s energized by the given feeder.
        :param feeder: The feeder for which to get the energized ``LvSubstation``s.
        :returns: A collection of ``LvSubstation``s energized by the given feeder.
        """

    @staticmethod
    @abstractmethod
    def add_equipment_to_container(equipment: Equipment, container: EquipmentContainer):
        """
         Adds the specified equipment to the given container.

         :param equipment: The equipment to add to the container.
         :param container: The container to which the equipment will be added.
        """

    @staticmethod
    @abstractmethod
    def add_container_to_equipment(container: EquipmentContainer, equipment: Equipment):
        """
        Adds the specified container to the given equipment.

        :param container: The container to add to the equipment.
        :param equipment: The equipment to which the container will be added.
        """

    @classmethod
    def associate_equipment_and_container(cls, equipment: Equipment, container: EquipmentContainer):
        """
        Establishes a bidirectional association between the specified equipment and container.

        :param equipment: The equipment to associate with the container.
        :param container: The container to associate with the equipment.
        """
        cls.add_equipment_to_container(equipment, container)
        cls.add_container_to_equipment(container, equipment)

    @staticmethod
    @abstractmethod
    def remove_equipment_from_container(equipment: Equipment, container: EquipmentContainer):
        """
        Removes the specified equipment from the given container.

        :param equipment: The equipment to remove from the container.
        :param container: The container from which the equipment will be removed.
        """

    @staticmethod
    @abstractmethod
    def remove_container_from_equipment(container: EquipmentContainer, equipment: Equipment):
        """
        Removes the specified container from the given equipment.

        :param container: The container to remove from the equipment.
        :param equipment: The equipment from which the container will be removed.
        """

    @classmethod
    def disassociate_equipment_and_container(cls, equipment: Equipment, container: EquipmentContainer):
        """
        Remove a bidirectional association between the specified equipment and container.

        :param equipment: The equipment to disassociate with the container.
        :param container: The container to disassociate with the equipment.
        """
        cls.remove_equipment_from_container(equipment, container)
        cls.remove_container_from_equipment(container, equipment)

    @staticmethod
    @abstractmethod
    def add_energizing_feeder_to_lv_feeder(feeder: Feeder, lv_feeder: LvFeeder):
        """
        Adds the specified energizing feeder to the given lvFeeder.

        :param feeder: The energizing feeder to add to the lvFeeder.
        :param lv_feeder: The lvFeeder to which the feeder will be added.
        """

    @staticmethod
    @abstractmethod
    def add_energizing_lv_feeder_to_feeder(lv_feeder: LvFeeder, feeder: Feeder):
        """
        Adds the specified energized lvFeeder to the given feeder.

        :param lv_feeder: The energized lvFeeder to add to the feeder.
        :param feeder: The feeder to which the lvFeeder will be added.
        """

    @staticmethod
    @abstractmethod
    def add_energizing_feeder_to_lv_substation(feeder: Feeder, lv_substation: LvSubstation):
        """
        Adds the specified energizing ``feeder`` to the given ``lv_substation``.

        :param feeder: The energizing ``feeder`` to add to the ``lv_substation``.
        :param lv_substation: The ``lv_substation`` to which the ``feeder`` will be added.
        """

    @staticmethod
    @abstractmethod
    def add_energized_lv_substation_to_feeder(lv_substation: LvSubstation, feeder: Feeder):
        """
        Adds the specified energized ``lv_substation`` to the given ``feeder``.

        :param lv_substation: The ``lv_substation`` to which the ``feeder`` will be added.
        :param feeder: The ``feeder`` to which the ``lv_substation`` will be added.
        """

    @staticmethod
    @abstractmethod
    def add_energizing_lv_substation_to_lv_feeder(lv_substation: LvSubstation, lv_feeder: LvFeeder):
        """
        Adds the specified ``lv_substation`` to the given ``lv_feeder``.

        :param lv_substation: The energizing ``lv_substation`` to add to the ``lv_feeder``.
        :param lv_feeder: The ``lv_feeder`` to add to the ``lv_substation``.
        """

    @staticmethod
    @abstractmethod
    def add_energized_lv_feeder_to_lv_substation(lv_feeder: LvFeeder, lv_substation: LvSubstation):
        """
        Adds the specified ``lv_feeder`` to the given ``lv_substation``.

        :param lv_feeder: The ``lv_feeder`` to which the ``lv_substation`` will be added.
        :param lv_substation: The ``lv_substation`` to which the ``lv_feeder`` will be added.
        """

    @classmethod
    def associate_energizing_feeder(cls, feeder: Feeder, other: LvFeeder | LvSubstation):
        """
        Establishes a bidirectional association between the specified feeder and LV feeder or LV substation.

        :param feeder: The feeder energizing the lv feeder.
        :param other: The lv feeder or substation energized by the feeder.
        """
        if isinstance(other, LvFeeder):
            cls.add_energizing_feeder_to_lv_feeder(feeder, other)
            cls.add_energizing_lv_feeder_to_feeder(other, feeder)
        elif isinstance(other, LvSubstation):
            cls.add_energizing_feeder_to_lv_substation(feeder, other)
            cls.add_energized_lv_substation_to_feeder(other, feeder)
        else:
            raise TypeError('`other` must be either LvFeeder or LvSubstation.')

    @classmethod
    def associate_energizing_lv_substation(cls, lv_feeder: LvFeeder, lv_substation: LvSubstation):
        """
        Establishes a bidirectional association between the specified ``lv_feeder`` and ``lv_substation``.
        :param lv_feeder: The ``LvFeeder`` energized by ``LvSubstation``.
        :param lv_substation: The ``LvSubstation`` energizing ``LvFeeder``.
        """
        cls.add_energizing_lv_substation_to_lv_feeder(lv_substation, lv_feeder)
        cls.add_energized_lv_feeder_to_lv_substation(lv_feeder, lv_substation)


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

    @singledispatchmethod
    @staticmethod
    def get_energizing_feeders(lv_feeder: LvFeeder) -> Generator[Feeder, None, None]:
        raise NotImplementedError()

    @get_energizing_feeders.register
    @staticmethod
    def _(lv_feeder: LvFeeder) -> Generator[Feeder, None, None]:
        return lv_feeder.normal_energizing_feeders

    @get_energizing_feeders.register
    @staticmethod
    def _(lv_substation: LvSubstation) -> Generator[Feeder, None, None]:
        return lv_substation.normal_energizing_feeders

    @staticmethod
    def get_energizing_lv_substation(lv_feeder: LvFeeder) -> LvSubstation | None:
        return lv_feeder.normal_energizing_lv_substation

    @singledispatchmethod
    @staticmethod
    def get_energized_lv_feeders(feeder: Feeder) -> Generator[LvFeeder, None, None]:
        raise NotImplementedError()

    @get_energized_lv_feeders.register
    @staticmethod
    def _(feeder: Feeder) -> Generator[LvFeeder, None, None]:
        return feeder.normal_energized_lv_feeders

    @get_energized_lv_feeders.register
    @staticmethod
    def _(lv_substation: LvSubstation) -> Generator[LvFeeder, None, None]:
        return lv_substation.normal_energized_lv_feeders

    @staticmethod
    def get_energized_lv_substations(feeder: Feeder) -> Generator[LvSubstation, None, None]:
        return feeder.normal_energized_lv_substations

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

    @staticmethod
    def add_energizing_feeder_to_lv_substation(feeder: Feeder, lv_substation: LvSubstation):
        lv_substation.add_normal_energizing_feeder(feeder)

    @staticmethod
    def add_energized_lv_substation_to_feeder(lv_substation: LvSubstation, feeder: Feeder):
        feeder.add_normal_energized_lv_substation(lv_substation)

    @staticmethod
    def add_energizing_lv_substation_to_lv_feeder(lv_substation: LvSubstation, lv_feeder: LvFeeder):
        lv_feeder.normal_energizing_lv_substation = lv_substation

    @staticmethod
    def add_energized_lv_feeder_to_lv_substation(lv_feeder: LvFeeder, lv_substation: LvSubstation):
        lv_substation.add_normal_energized_lv_feeder(lv_feeder)


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

    @singledispatchmethod
    @staticmethod
    def get_energizing_feeders(lv_feeder: LvFeeder) -> Generator[Feeder, None, None]:
        raise NotImplementedError()

    @get_energizing_feeders.register
    @staticmethod
    def _(lv_feeder: LvFeeder) -> Generator[Feeder, None, None]:
        return lv_feeder.current_energizing_feeders

    @get_energizing_feeders.register
    @staticmethod
    def _(lv_substation: LvSubstation) -> Generator[Feeder, None, None]:
        return lv_substation.current_energizing_feeders

    @staticmethod
    def get_energizing_lv_substation(lv_feeder: LvFeeder) -> LvSubstation | None:
        return lv_feeder.normal_energizing_lv_substation

    @singledispatchmethod
    @staticmethod
    def get_energized_lv_feeders(feeder: Feeder | LvSubstation) -> Generator[LvFeeder, None, None]:
        raise NotImplementedError()

    @get_energized_lv_feeders.register
    @staticmethod
    def _(feeder: Feeder) -> Generator[LvFeeder, None, None]:
        return feeder.current_energized_lv_feeders

    @get_energized_lv_feeders.register
    @staticmethod
    def _(lv_substation: LvSubstation) -> Generator[LvFeeder, None, None]:
        return lv_substation.normal_energized_lv_feeders

    @staticmethod
    def get_energized_lv_substations(feeder: Feeder) -> Generator[LvSubstation, None, None]:
        return feeder.current_energized_lv_substations

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

    @staticmethod
    def add_energizing_feeder_to_lv_substation(feeder: Feeder, lv_substation: LvSubstation):
        lv_substation.add_current_energizing_feeder(feeder)

    @staticmethod
    def add_energized_lv_substation_to_feeder(lv_substation: LvSubstation, feeder: Feeder):
        feeder.add_current_energized_lv_substation(lv_substation)

    @staticmethod
    def add_energizing_lv_substation_to_lv_feeder(lv_substation: LvSubstation, lv_feeder: LvFeeder):
        lv_feeder.normal_energizing_lv_substation = lv_substation

    @staticmethod
    def add_energized_lv_feeder_to_lv_substation(lv_feeder: LvFeeder, lv_substation: LvSubstation):
        lv_substation.add_normal_energized_lv_feeder(lv_feeder)


EquipmentContainerStateOperators.NORMAL = NormalEquipmentContainerStateOperators
EquipmentContainerStateOperators.CURRENT = CurrentEquipmentContainerStateOperators
