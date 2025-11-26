#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ['EquipmentContainer']

from typing import Optional, Dict, Generator, List, TYPE_CHECKING, TypeVar

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61970.base.core.connectivity_node_container import ConnectivityNodeContainer
from zepben.ewb.util import nlen, ngen, safe_remove_by_id

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.equipment import Equipment
    from zepben.ewb.model.cim.iec61970.base.core.feeder import Feeder
    from zepben.ewb.model.cim.extensions.iec61970.base.feeder.lv_feeder import LvFeeder

T = TypeVar("T")


@dataslot
class EquipmentContainer(ConnectivityNodeContainer):
    """
    A modeling construct to provide a root class for containing equipment.
    Unless overridden, all functions operating on currentEquipment simply operate on the equipment collection. i.e. currentEquipment = equipment
    """

    equipment: List[Equipment] | None = MRIDDictAccessor()
    """Map of Equipment in this EquipmentContainer by their mRID"""

    def _retype(self):
        self.equipment: MRIDDictRouter[Equipment] = ...
    
    @deprecated("BOILERPLATE: Use len(equipment) instead")
    def num_equipment(self):
        return len(self.equipment)

    @deprecated("BOILERPLATE: Use equipment.get_by_mrid(mrid) instead")
    def get_equipment(self, mrid: str) -> Equipment:
        """
        Get the `Equipment` for this `EquipmentContainer` identified by `mrid`

        `mrid` the mRID of the required `Equipment`
        Returns The `Equipment` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return self.equipment.get_by_mrid(mrid)

    @custom_add(equipment)
    def add_equipment(self, equipment: Equipment) -> EquipmentContainer:
        """
        Associate `equipment` with this `EquipmentContainer`.

        `equipment` The `Equipment` to associate with this `EquipmentContainer`.
        Returns A reference to this `EquipmentContainer` to allow fluent use.
        Raises `ValueError` if another `Equipment` with the same `mrid` already exists for this `EquipmentContainer`.
        """
        if self._validate_reference(equipment, self.get_equipment, "An Equipment"):
            return self
        self.equipment.append_unchecked(equipment)
        return self

    @deprecated("Boilerplate: Use equipment.remove(equipment) instead")
    def remove_equipment(self, equipment: Equipment) -> EquipmentContainer:
        self.equipment.remove(equipment)
        return self

    @deprecated("BOILERPLATE: Use equipment.clear() instead")
    def clear_equipment(self) -> EquipmentContainer:
        self.equipment.clear()
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
        for equip in self.equipment:
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
        for equip in self.equipment:
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
        for equip in self.equipment:
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
        for equip in self.equipment:
            for f in equip.normal_lv_feeders:
                if f not in seen:
                    seen.add(f.mrid)
                    yield f
