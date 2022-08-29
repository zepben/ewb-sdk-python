#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional, Dict, Generator, List, TYPE_CHECKING

if TYPE_CHECKING:
    from zepben.evolve import Equipment, Terminal, Substation, LvFeeder

from zepben.evolve.model.cim.iec61970.base.core.connectivity_node_container import ConnectivityNodeContainer
from zepben.evolve.util import nlen, ngen, safe_remove_by_id

__all__ = ['EquipmentContainer', 'Feeder', 'Site']


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
        return ngen(self._equipment.values() if self._equipment is not None else None)

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
        self._equipment = dict() if self._equipment is None else self._equipment
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
        Convenience function to find all of the normal LV feeders of the equipment associated with this equipment container.
        Returns the normal LV feeders for all associated LV feeders
        """
        seen = set()
        for equip in self._equipment.values():
            for f in equip.normal_lv_feeders:
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
    """The equipment contained in this feeder in the current state of the network."""

    _normal_energized_lv_feeders: Optional[Dict[str, LvFeeder]] = None
    """The LV feeders that are energized by this feeder in the normal state of the network."""

    def __init__(
        self,
        normal_head_terminal: Terminal = None,
        normal_energizing_substation: Substation = None,
        current_equipment: List[Equipment] = None,
        normal_energized_lv_feeders: List[LvFeeder] = None,
        **kwargs
    ):
        super(Feeder, self).__init__(**kwargs)
        if normal_head_terminal:
            self.normal_head_terminal = normal_head_terminal
        if normal_energizing_substation:
            self.normal_energizing_substation = normal_energizing_substation
        if normal_energized_lv_feeders:
            for lv_feeder in normal_energized_lv_feeders:
                self.add_normal_energized_lv_feeder(lv_feeder)
        if current_equipment:
            for eq in current_equipment:
                self.add_current_equipment(eq)

    @property
    def normal_head_terminal(self) -> Optional[Terminal]:
        """The normal head terminal or terminals of the feeder."""
        return self._normal_head_terminal

    @normal_head_terminal.setter
    def normal_head_terminal(self, term: Optional[Terminal]):
        if self._normal_head_terminal is None or self._normal_head_terminal is term:
            self._normal_head_terminal = term
        else:
            raise ValueError(f"normal_head_terminal for {str(self)} has already been set to {self._normal_head_terminal}, cannot reset this field to {term}")

    @property
    def current_equipment(self) -> Generator[Equipment, None, None]:
        """
        Contained `Equipment` using the current state of the network.
        """
        return ngen(self._current_equipment.values() if self._current_equipment is not None else None)

    def num_current_equipment(self):
        """
        Returns The number of `Equipment` associated with this `Feeder`
        """
        return nlen(self._current_equipment)

    def get_current_equipment(self, mrid: str) -> Equipment:
        """
        Get the `Equipment` for this `Feeder` identified by `mrid`

        `mrid` The mRID of the required `Equipment`
        Returns The `Equipment` with the specified `mrid` if it exists
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

        `equipment` the `Equipment` to associate with this `Feeder`.
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

        `equipment` The `Equipment` to disassociate from this `Feeder`.
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

    @property
    def normal_energized_lv_feeders(self) -> Generator[LvFeeder, None, None]:
        """
        The LV feeders that are energized by this feeder.
        """
        return ngen(self._normal_energized_lv_feeders.values() if self._normal_energized_lv_feeders is not None else self._normal_energized_lv_feeders)

    def num_normal_energized_lv_feeders(self) -> int:
        """
        Get the number of LV feeders that are energized by this feeder.
        """
        return nlen(self._normal_energized_lv_feeders)

    def get_normal_energized_lv_feeder(self, mrid: str) -> LvFeeder:
        """
        Energized LvFeeder in the normal state of the network.

        @param mrid: The mrid of the `LvFeeder`.
        @return A matching `LvFeeder` that is energized by this `Feeder` in the normal state of the network.
        @raise A `KeyError` if no matching `LvFeeder` was found.
        """
        if not self._normal_energized_lv_feeders:
            raise KeyError(mrid)
        try:
            return self._normal_energized_lv_feeders[mrid]
        except AttributeError:
            raise KeyError(mrid)

    def add_normal_energized_lv_feeder(self, lv_feeder: LvFeeder) -> Feeder:
        """
        Associate this `Feeder` with an `LvFeeder` in the normal state of the network.

        @param lv_feeder: the LV feeder to associate with this feeder in the normal state of the network.
        @return: This `Feeder` for fluent use.
        """
        if self._validate_reference(lv_feeder, self.get_normal_energized_lv_feeder, "An LvFeeder"):
            return self
        self._normal_energized_lv_feeders = dict() if self._normal_energized_lv_feeders is None else self._normal_energized_lv_feeders
        self._normal_energized_lv_feeders[lv_feeder.mrid] = lv_feeder
        return self

    def remove_normal_energized_lv_feeder(self, lv_feeder: LvFeeder) -> Feeder:
        """
        Disassociate this `Feeder` from an `LvFeeder` in the normal state of the network.

        @param lv_feeder: the LV feeder to disassociate from this feeder in the normal state of the network.
        @return: This `Feeder` for fluent use.
        @raise: A `ValueError` if `lv_feeder` is not found in the normal energized lv feeders collection.
        """
        self._normal_energized_lv_feeders = safe_remove_by_id(self._normal_energized_lv_feeders, lv_feeder)
        return self

    def clear_normal_energized_lv_feeders(self) -> Feeder:
        """
        Clear all `LvFeeder`s associated with `Feeder` in the normal state of the network.

        @return: This `Feeder` for fluent use.
        """
        self._normal_energized_lv_feeders = None
        return self


class Site(EquipmentContainer):
    """
    A collection of equipment for organizational purposes, used for grouping distribution resources located at a site.
    Note this is not a CIM concept - however represents an `EquipmentContainer` in CIM. This is to avoid the use of `EquipmentContainer` as a concrete class.
    """
    pass
