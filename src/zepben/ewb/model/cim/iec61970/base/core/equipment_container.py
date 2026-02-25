#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ['EquipmentContainer']

from typing import Optional, Dict, Generator, List, TYPE_CHECKING, TypeVar, Iterable, Type

from zepben.ewb.model.cim.iec61970.base.core.connectivity_node_container import ConnectivityNodeContainer
from zepben.ewb.util import nlen, ngen, safe_remove_by_id

if TYPE_CHECKING:
    from zepben.ewb.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
    from zepben.ewb.model.cim.iec61970.base.core.equipment import Equipment
    from zepben.ewb.model.cim.iec61970.base.core.feeder import Feeder
    from zepben.ewb.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
    from zepben.ewb.model.cim.iec61970.base.core.terminal import Terminal
    from zepben.ewb.model.cim.extensions.iec61970.base.feeder.lv_feeder import LvFeeder

T = TypeVar("T")


class EquipmentContainer(ConnectivityNodeContainer):
    """
    A modeling construct to provide a root class for containing equipment.
    Unless overridden, all functions operating on currentEquipment simply operate on the equipment collection. i.e. currentEquipment = equipment
    """

    _equipment: Optional[Dict[str, Equipment]] = None
    """Map of Equipment in this EquipmentContainer by their mRID"""

    def __init__(self, equipment: List[Equipment] = None, **kwargs):
        super(EquipmentContainer, self).__init__(**kwargs)
        if equipment:
            for eq in equipment:
                self.add_equipment(eq)

    def num_equipment(self):
        """
        Returns The number of `Equipment` associated with this `EquipmentContainer`
        """
        return nlen(self._equipment)

    @property
    def equipment(self) -> Generator[Equipment, None, None]:
        """
        The `Equipment` contained in this `EquipmentContainer`
        """
        return ngen(self._equipment)

    def get_equipment(self, mrid: str) -> Equipment:
        """
        Get the `Equipment` for this `EquipmentContainer` identified by `mrid`

        `mrid` the mRID of the required `Equipment`
        Returns The `Equipment` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        if not self._equipment:
            raise KeyError(mrid)
        try:
            return self._equipment[mrid]
        except AttributeError:
            raise KeyError(mrid)

    def add_equipment(self, equipment: Equipment) -> EquipmentContainer:
        """
        Associate `equipment` with this `EquipmentContainer`.

        `equipment` The `Equipment` to associate with this `EquipmentContainer`.
        Returns A reference to this `EquipmentContainer` to allow fluent use.
        Raises `ValueError` if another `Equipment` with the same `mrid` already exists for this `EquipmentContainer`.
        """
        if self._validate_reference(equipment, self.get_equipment, "An Equipment"):
            return self
        if self._equipment is None:
            self._equipment = dict()
        self._equipment[equipment.mrid] = equipment
        return self

    def remove_equipment(self, equipment: Equipment) -> EquipmentContainer:
        """
        Disassociate `equipment` from this `EquipmentContainer`

        `equipment` The `Equipment` to disassociate with this `EquipmentContainer`.
        Returns A reference to this `EquipmentContainer` to allow fluent use.
        Raises `KeyError` if `equipment` was not associated with this `EquipmentContainer`.
        """
        self._equipment = safe_remove_by_id(self._equipment, equipment)
        return self

    def clear_equipment(self) -> EquipmentContainer:
        """
        Clear all equipment.
        Returns A reference to this `EquipmentContainer` to allow fluent use.
        """
        self._equipment = None
        return self

    @property
    def current_equipment(self) -> Generator[Equipment, None, None]:
        """
        Contained `Equipment` using the current state of the network.
        """
        return self.equipment

    def num_current_equipment(self) -> int:
        """
        Returns The number of `Equipment` contained in this `EquipmentContainer` in the current state of the network.
        """
        return self.num_equipment()

    def get_current_equipment(self, mrid: str) -> Equipment:
        """
        Get the `Equipment` contained in this `EquipmentContainer` in the current state of the network, identified by `mrid`

        `mrid` The mRID of the required `Equipment`
        Returns The `Equipment` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return self.get_equipment(mrid)

    def add_current_equipment(self, equipment: Equipment) -> EquipmentContainer:
        """
        Associate `equipment` with this `EquipmentContainer` in the current state of the network.

        `equipment` the `Equipment` to associate with this `EquipmentContainer` in the current state of the network.
        Returns A reference to this `EquipmentContainer` to allow fluent use.
        Raises `ValueError` if another `Equipment` with the same `mrid` already exists for this `EquipmentContainer`.
        """
        self.add_equipment(equipment)
        return self

    def remove_current_equipment(self, equipment: Equipment) -> EquipmentContainer:
        """
        Disassociate `equipment` from this `EquipmentContainer` in the current state of the network.

        `equipment` The `Equipment` to disassociate from this `EquipmentContainer` in the current state of the network.
        Returns A reference to this `EquipmentContainer` to allow fluent use.
        Raises `KeyError` if `equipment` was not associated with this `EquipmentContainer`.
        """
        self.remove_equipment(equipment)
        return self

    def clear_current_equipment(self) -> EquipmentContainer:
        """
        Clear all `Equipment` from this `EquipmentContainer` in the current state of the network.
        Returns A reference to this `EquipmentContainer` to allow fluent use.
        """
        self.clear_equipment()
        return self

    def current_feeders(self) -> Generator[Feeder, None, None]:
        """
        Convenience function to find all of the current feeders of the equipment associated with this equipment container.
        Returns the current feeders for all associated feeders
        """
        seen = set()
        for equip in self._equipment.values():
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
        for equip in self._equipment.values():
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
        for equip in self._equipment.values():
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
        for equip in self._equipment.values():
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

        for it in state_operator.get_equipment(self):
            if isinstance(it, ConductingEquipment):
                for t in it.terminals:
                    for ct in NetworkService.connected_terminals(t):
                        if (to := ct.to_equip) and to.get_container(self.mrid) is None:
                            yield ct.from_terminal
