#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Feeder"]

from typing import Optional, Dict, TYPE_CHECKING

from zepben.ewb.collections.autoslot import dataslot, ValidatedDescriptor
from zepben.ewb.collections.mrid_dict import MRIDDict
from zepben.ewb.model.cim.iec61970.base.core.equipment_container import EquipmentContainer

if TYPE_CHECKING:
    from zepben.ewb.model.cim.extensions.iec61970.base.feeder.lv_feeder import LvFeeder
    from zepben.ewb.model.cim.iec61970.base.core.equipment import Equipment
    from zepben.ewb.model.cim.iec61970.base.core.substation import Substation
    from zepben.ewb.model.cim.iec61970.base.core.terminal import Terminal


@dataslot
class Feeder(EquipmentContainer):
    """
    A collection of equipment for organizational purposes, used for grouping distribution resources.
    The organization of a feeder does not necessarily reflect connectivity or current operation state.
    """
    def __validate_normal_head_terminal(self, term: Optional[Terminal]):
        if self.normal_head_terminal is None or self.normal_head_terminal is term or (self.num_equipment() == 0 and self.num_current_equipment() == 0):
            return term
        else:
            raise ValueError(f"Feeder {self.mrid} has equipment assigned to it. Cannot update normalHeadTerminal on a feeder with equipment assigned.")
    normal_head_terminal: Optional[Terminal] = ValidatedDescriptor(validate=__validate_normal_head_terminal)
    """The normal head terminal or terminals of the feeder."""

    normal_energizing_substation: Optional[Substation] = None
    """The substation that nominally energizes the feeder. Also used for naming purposes."""

    current_equipment: Optional[Dict[str, Equipment]] = None
    """The equipment contained in this feeder in the current state of the network."""

    normal_energized_lv_feeders: Optional[Dict[str, LvFeeder]] = None
    """The LV feeders that are energized by this feeder in the normal state of the network."""

    current_energized_lv_feeders: Optional[Dict[str, LvFeeder]] = None
    """The LV feeders that are energized by this feeder in the current state of the network."""

    def __post_init__(self, normal_head_terminal: Terminal = None):
        if normal_head_terminal:
            self.normal_head_terminal = normal_head_terminal
        self.current_equipment: MRIDDict[Equipment] = MRIDDict(self.current_equipment)
        self.normal_energized_lv_feeders: MRIDDict[LvFeeder] = MRIDDict(self.normal_energized_lv_feeders)
        self.current_energized_lv_feeders: MRIDDict[LvFeeder] = MRIDDict(self.current_energized_lv_feeders)

    # @property
    # def normal_head_terminal(self) -> Optional[Terminal]:
    #     """The normal head terminal or terminals of the feeder."""
    #     return self._normal_head_terminal

    # @normal_head_terminal.setter
    # def normal_head_terminal(self, term: Optional[Terminal]):
    #     if self._normal_head_terminal is None or self._normal_head_terminal is term or (self.num_equipment() == 0 and self.num_current_equipment() == 0):
    #         self._normal_head_terminal = term
    #     else:
    #         raise ValueError(f"Feeder {self.mrid} has equipment assigned to it. Cannot update normalHeadTerminal on a feeder with equipment assigned.")

    def num_current_equipment(self):
        """
        Returns The number of `Equipment` associated with this `Feeder`
        """
        return len(self.current_equipment)

    def get_current_equipment(self, mrid: str) -> Equipment:
        """
        Get the `Equipment` for this `Feeder` identified by `mrid`

        `mrid` The mRID of the required `Equipment`
        Returns The `Equipment` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return self.current_equipment.get_by_mrid(mrid)

    def add_current_equipment(self, equipment: Equipment) -> Feeder:
        """
        Associate `equipment` with this `Feeder`.

        `equipment` the `Equipment` to associate with this `Feeder`.
        Returns A reference to this `Feeder` to allow fluent use.
        Raises `ValueError` if another `Equipment` with the same `mrid` already exists for this `Feeder`.
        """
        self.current_equipment.add(equipment)
        return self

    def remove_current_equipment(self, equipment: Equipment) -> Feeder:
        """
        Disassociate `equipment` from this `Feeder`

        `equipment` The `Equipment` to disassociate from this `Feeder`.
        Returns A reference to this `Feeder` to allow fluent use.
        Raises `KeyError` if `equipment` was not associated with this `Feeder`.
        """
        self.current_equipment.remove(equipment)
        return self

    def clear_current_equipment(self) -> Feeder:
        """
        Clear all equipment.
        Returns A reference to this `Feeder` to allow fluent use.
        """
        self.current_equipment.clear()
        return self

    def num_normal_energized_lv_feeders(self) -> int:
        """
        Get the number of LV feeders that are normally energized by this feeder.
        """
        return len(self.normal_energized_lv_feeders)

    def get_normal_energized_lv_feeder(self, mrid: str) -> LvFeeder:
        """
        Energized LvFeeder in the normal state of the network.

        @param mrid: The mrid of the `LvFeeder`.
        @return A matching `LvFeeder` that is energized by this `Feeder` in the normal state of the network.
        @raise A `KeyError` if no matching `LvFeeder` was found.
        """
        return self.normal_energized_lv_feeders.get_by_mrid(mrid)

    def add_normal_energized_lv_feeder(self, lv_feeder: LvFeeder) -> Feeder:
        """
        Associate this `Feeder` with an `LvFeeder` in the normal state of the network.

        @param lv_feeder: the LV feeder to associate with this feeder in the normal state of the network.
        @return: This `Feeder` for fluent use.
        """
        self.normal_energized_lv_feeders.add(lv_feeder)
        return self

    def remove_normal_energized_lv_feeder(self, lv_feeder: LvFeeder) -> Feeder:
        """
        Disassociate this `Feeder` from an `LvFeeder` in the normal state of the network.

        @param lv_feeder: the LV feeder to disassociate from this feeder in the normal state of the network.
        @return: This `Feeder` for fluent use.
        @raise: A `ValueError` if `lv_feeder` is not found in the normal energized lv feeders collection.
        """
        self.normal_energized_lv_feeders.remove(lv_feeder)
        return self

    def clear_normal_energized_lv_feeders(self) -> Feeder:
        """
        Clear all `LvFeeder`s associated with `Feeder` in the normal state of the network.

        @return: This `Feeder` for fluent use.
        """
        self.normal_energized_lv_feeders.clear()
        return self

    def num_current_energized_lv_feeders(self) -> int:
        """
        Get the number of LV feeders that are currently energized by this feeder.
        """
        return len(self.current_energized_lv_feeders)

    def get_current_energized_lv_feeder(self, mrid: str) -> LvFeeder:
        """
        Energized LvFeeder in the current state of the network.

        @param mrid: The mrid of the `LvFeeder`.
        @return A matching `LvFeeder` that is energized by this `Feeder` in the current state of the network.
        @raise A `KeyError` if no matching `LvFeeder` was found.
        """
        return self.current_energized_lv_feeders.get_by_mrid(mrid)

    def add_current_energized_lv_feeder(self, lv_feeder: LvFeeder) -> Feeder:
        """
        Associate this `Feeder` with an `LvFeeder` in the current state of the network.

        @param lv_feeder: the LV feeder to associate with this feeder in the current state of the network.
        @return: This `Feeder` for fluent use.
        """
        self.current_energized_lv_feeders.add(lv_feeder)
        return self

    def remove_current_energized_lv_feeder(self, lv_feeder: LvFeeder) -> Feeder:
        """
        Disassociate this `Feeder` from an `LvFeeder` in the current state of the network.

        @param lv_feeder: the LV feeder to disassociate from this feeder in the current state of the network.
        @return: This `Feeder` for fluent use.
        @raise: A `ValueError` if `lv_feeder` is not found in the current energized lv feeders collection.
        """
        self.current_energized_lv_feeders.add(lv_feeder)
        return self

    def clear_current_energized_lv_feeders(self) -> Feeder:
        """
        Clear all `LvFeeder`s associated with `Feeder` in the current state of the network.

        @return: This `Feeder` for fluent use.
        """
        self.current_energized_lv_feeders.clear()
        return self
