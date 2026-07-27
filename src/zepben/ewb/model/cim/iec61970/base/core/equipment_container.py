#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ['EquipmentContainer']

from dataclasses import field
from typing import Dict, Generator, TYPE_CHECKING, TypeVar, Iterable, Type
from abc import ABCMeta

from typing_extensions import deprecated

from zepben.ewb import Alias
from zepben.ewb.boilerplate.collections.mrid_list import MridCollection
from zepben.ewb.boilerplate.collections.mrid_map import LazyMridMap
from zepben.ewb.model.cim.iec61970.base.core.connectivity_node_container import ConnectivityNodeContainer
from zepben.ewb.boilerplate.dataclass_base import zb_dataclass

if TYPE_CHECKING:
    from zepben.ewb.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
    from zepben.ewb.model.cim.iec61970.base.core.equipment import Equipment
    from zepben.ewb.model.cim.iec61970.base.core.feeder import Feeder
    from zepben.ewb.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
    from zepben.ewb.model.cim.iec61970.base.core.terminal import Terminal
    from zepben.ewb.model.cim.extensions.iec61970.base.feeder.lv_feeder import LvFeeder

T = TypeVar("T")


@zb_dataclass
class EquipmentContainer(ConnectivityNodeContainer, metaclass=ABCMeta):
    """
    A modeling construct to provide a root class for containing equipment.
    Unless overridden, all functions operating on currentEquipment simply operate on the equipment collection. i.e. currentEquipment = equipment
    """

    _equipment_by_id: Dict[str, Equipment] | None = field(default=None)
    """Map of Equipment in this EquipmentContainer by their mRID"""

    equipment: MridCollection[Equipment] = LazyMridMap(
        _equipment_by_id,
        "An Equipment",
    )
    """The `Equipment` contained in this `EquipmentContainer`"""

    current_equipment = Alias(equipment)
    """Contained `Equipment` using the current state of the network."""

    def current_feeders(self) -> Generator[Feeder, None, None]:
        """
        Convenience function to find all of the current feeders of the equipment associated with this equipment container.
        Returns the current feeders for all associated feeders
        """
        seen = set()
        for equip in self._equipment_by_id.values():
            for f in equip.current_feeders:
                if f not in seen:
                    seen.add(f.mrid)
                    yield f

    def normal_feeders(self) -> Generator[Feeder, None, None]:
        """
        Convenience function to find all of the normal feeders of the equipment associated with this equipment container.
        Returns the normal feeders for all associated feeders
        """
        seen = set()
        for equip in self._equipment_by_id.values():
            for f in equip.normal_feeders:
                if f not in seen:
                    seen.add(f.mrid)
                    yield f

    def current_lv_feeders(self) -> Generator[LvFeeder, None, None]:
        """
        Convenience function to find all of the normal LV feeders of the equipment associated with this equipment container.
        Returns the normal LV feeders for all associated LV feeders
        """
        seen = set()
        for equip in self._equipment_by_id.values():
            for f in equip.current_lv_feeders:
                if f not in seen:
                    seen.add(f.mrid)
                    yield f

    def normal_lv_feeders(self) -> Generator[LvFeeder, None, None]:
        """
        Convenience function to find all the normal LV feeders of the equipment associated with this equipment container.
        Returns the normal LV feeders for all associated LV feeders
        """
        seen = set()
        for equip in self._equipment_by_id.values():
            for f in equip.normal_lv_feeders:
                if f not in seen:
                    seen.add(f.mrid)
                    yield f

    def find_lv_feeders(
        self,
        lv_feeder_start_points: Iterable['ConductingEquipment'],
        state_operators: Type['NetworkStateOperators']
    ) -> Generator['LvFeeder', None, None]:
        # NOTE: this import exists due to a circular import problem.
        from zepben.ewb.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
        for ce in state_operators.get_equipment(self):
            if isinstance(ce, ConductingEquipment):
                if ce in lv_feeder_start_points:
                    if not state_operators.is_open(ce):  # Exclude any open switch that might be energised by a different feeder on the other side
                        for lv_feeder in ce.lv_feeders(state_operators):
                            yield lv_feeder

    def edge_terminals(self, state_operator: 'Type[NetworkStateOperators]' = None) -> Generator['Terminal', None, None]:
        """
        Retrieve all terminals that are located on the edge of this EquipmentContainer. This is determined by any terminal that connects to another terminal on a
        ConductingEquipment that is not a member of this EquipmentContainer. This will explicitly exclude equipment with only one terminal that do not
        provide connectivity to the rest of the network.

        :param state_operator: The network state to operate on.
        """

        # NOTE: these imports and lazy state operator setting exist due to a circular import problem.
        from zepben.ewb.services.network.network_service import NetworkService
        from zepben.ewb.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
        from zepben.ewb.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
        if state_operator is None:
            state_operator = NetworkStateOperators.NORMAL

        seen: set = set()
        for it in state_operator.get_equipment(self):
            if isinstance(it, ConductingEquipment):
                for t in it.terminals:
                    for ct in NetworkService.connected_terminals(t):
                        if to := ct.to_equip:
                            try:
                                to.get_container(self.mrid)
                            except KeyError:
                                if t not in seen:
                                    seen.add(ct.from_terminal)
                                    yield ct.from_terminal



    # region deprecated list boilerplate
    # region equipment boilerplate

    @deprecated("Use len(self.equipment) instead")
    def num_equipment(self):
        return len(self.equipment)

    @deprecated("Use self.equipment.get_by_mrid(mrid) instead")
    def get_equipment(self, mrid: str) -> Equipment:
        return self.equipment.get_by_mrid(mrid)

    @deprecated("Use equipment.append(equipment) instead")
    def add_equipment(self, equipment: Equipment) -> EquipmentContainer:
        self.equipment.append(equipment)
        return self

    @deprecated("Use equipment.remove(equipment) instead")
    def remove_equipment(self, equipment: Equipment) -> EquipmentContainer:
        self.equipment.remove(equipment)
        return self

    @deprecated("Use equipment.clear() instead")
    def clear_equipment(self) -> EquipmentContainer:
        self.equipment.clear()
        return self

    # endregion
    # region current_equipment boilerplate

    @deprecated("Use len(current_equipment) instead")
    def num_current_equipment(self):
        return len(self.current_equipment)

    @deprecated("Use current_equipment.get_by_mrid(mrid) instead")
    def get_current_equipment(self, mrid: str) -> Equipment:
        return self.current_equipment.get_by_mrid(mrid)

    @deprecated("Use current_equipment.append(equipment) instead")
    def add_current_equipment(self, equipment: Equipment) -> EquipmentContainer:
        self.current_equipment.append(equipment)
        return self

    @deprecated("Use current_equipment.remove(equipment) instead")
    def remove_current_equipment(self, equipment: Equipment) -> EquipmentContainer:
        self.current_equipment.remove(equipment)
        return self

    @deprecated("Use current_equipment.clear() instead")
    def clear_current_equipment(self) -> EquipmentContainer:
        self.current_equipment.clear()
        return self

    # endregion
    # endregion
