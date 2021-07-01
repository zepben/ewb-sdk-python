#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional, Dict, Generator, List, TYPE_CHECKING

if TYPE_CHECKING:
    from zepben.evolve import Equipment, Terminal, Substation

from zepben.evolve.model.cim.iec61970.base.core.connectivity_node_container import ConnectivityNodeContainer
from zepben.evolve.util import nlen, ngen, safe_remove_by_id

__all__ = ['EquipmentContainer', 'Feeder', 'Site']


class EquipmentContainer(ConnectivityNodeContainer):
    """
    A modeling construct to provide a root class for containing equipment.
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
        Returns The number of `zepben.evolve.iec61970.base.core.equipment.Equipment` associated with this `EquipmentContainer`
        """
        return nlen(self._equipment)

    @property
    def equipment(self) -> Generator[Equipment, None, None]:
        """
        The `zepben.evolve.iec61970.base.core.equipment.Equipment` contained in this `EquipmentContainer`
        """
        return ngen(self._equipment.values() if self._equipment is not None else None)

    def get_equipment(self, mrid: str) -> Equipment:
        """
        Get the `zepben.evolve.iec61970.base.core.equipment.Equipment` for this `EquipmentContainer` identified by `mrid`

        `mrid` the mRID of the required `zepben.evolve.iec61970.base.core.equipment.Equipment`
        Returns The `zepben.evolve.iec61970.base.core.equipment.Equipment` with the specified `mrid` if it exists
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

        `equipment` The `zepben.evolve.iec61970.base.core.equipment.Equipment` to associate with this `EquipmentContainer`.
        Returns A reference to this `EquipmentContainer` to allow fluent use.
        Raises `ValueError` if another `Equipment` with the same `mrid` already exists for this `EquipmentContainer`.
        """
        if self._validate_reference(equipment, self.get_equipment, "An Equipment"):
            return self
        self._equipment = dict() if self._equipment is None else self._equipment
        self._equipment[equipment.mrid] = equipment
        return self

    def remove_equipment(self, equipment: Equipment) -> EquipmentContainer:
        """
        Disassociate `equipment` from this `EquipmentContainer`

        `equipment` The `zepben.evolve.iec61970.base.core.equipment.Equipment` to disassociate with this `EquipmentContainer`.
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


class Feeder(EquipmentContainer):
    """
    A collection of equipment for organizational purposes, used for grouping distribution resources.
    The organization of a feeder does not necessarily reflect connectivity or current operation state.
    """

    _normal_head_terminal: Optional[Terminal] = None
    """The normal head terminal or terminals of the feeder."""

    normal_energizing_substation: Optional[Substation] = None
    """The substation that nominally energizes the feeder. Also used for naming purposes."""

    _current_equipment: Optional[Dict[str, Equipment]] = None

    def __init__(self, normal_head_terminal: Terminal = None, current_equipment: List[Equipment] = None, **kwargs):
        super(Feeder, self).__init__(**kwargs)
        if normal_head_terminal:
            self.normal_head_terminal = normal_head_terminal
        if current_equipment:
            for eq in current_equipment:
                self.add_current_equipment(eq)

    @property
    def normal_head_terminal(self):
        """The normal head terminal or terminals of the feeder."""
        return self._normal_head_terminal

    @normal_head_terminal.setter
    def normal_head_terminal(self, term):
        if self._normal_head_terminal is None or self._normal_head_terminal is term:
            self._normal_head_terminal = term
        else:
            raise ValueError(f"normal_head_terminal for {str(self)} has already been set to {self._normal_head_terminal}, cannot reset this field to {term}")

    @property
    def current_equipment(self) -> Generator[Equipment, None, None]:
        """
        Contained `zepben.evolve.iec61970.base.core.equipment.Equipment` using the current state of the network.
        """
        return ngen(self._current_equipment.values() if self._current_equipment is not None else None)

    def num_current_equipment(self):
        """
        Returns The number of `zepben.evolve.iec61970.base.core.equipment.Equipment` associated with this `Feeder`
        """
        return nlen(self._current_equipment)

    def get_current_equipment(self, mrid: str) -> Equipment:
        """
        Get the `zepben.evolve.iec61970.base.core.equipment.Equipment` for this `Feeder` identified by `mrid`

        `mrid` The mRID of the required `zepben.evolve.iec61970.base.core.equipment.Equipment`
        Returns The `zepben.evolve.iec61970.base.core.equipment.Equipment` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        if not self._current_equipment:
            raise KeyError(mrid)
        try:
            return self._current_equipment[mrid]
        except AttributeError:
            raise KeyError(mrid)

    def add_current_equipment(self, equipment: Equipment) -> Feeder:
        """
        Associate `equipment` with this `Feeder`.

        `equipment` the `zepben.evolve.iec61970.base.core.equipment.Equipment` to associate with this `Feeder`.
        Returns A reference to this `Feeder` to allow fluent use.
        Raises `ValueError` if another `Equipment` with the same `mrid` already exists for this `Feeder`.
        """
        if self._validate_reference(equipment, self.get_current_equipment, "An Equipment"):
            return self
        self._current_equipment = dict() if self._current_equipment is None else self._current_equipment
        self._current_equipment[equipment.mrid] = equipment
        return self

    def remove_current_equipment(self, equipment: Equipment) -> Feeder:
        """
        Disassociate `equipment` from this `Feeder`

        `equipment` The `equipment.Equipment` to disassociate from this `Feeder`.
        Returns A reference to this `Feeder` to allow fluent use.
        Raises `KeyError` if `equipment` was not associated with this `Feeder`.
        """
        self._current_equipment = safe_remove_by_id(self._current_equipment, equipment)
        return self

    def clear_current_equipment(self) -> Feeder:
        """
        Clear all equipment.
        Returns A reference to this `Feeder` to allow fluent use.
        """
        self._current_equipment = None
        return self


class Site(EquipmentContainer):
    """
    A collection of equipment for organizational purposes, used for grouping distribution resources located at a site.
    Note this is not a CIM concept - however represents an `EquipmentContainer` in CIM. This is to avoid the use of `EquipmentContainer` as a concrete class.
    """
    pass
