#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Feeder"]

from typing import Optional, Dict, List, Generator, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61970.base.core.equipment_container import EquipmentContainer
from zepben.ewb.util import ngen, nlen, safe_remove_by_id

if TYPE_CHECKING:
    from zepben.ewb.model.cim.extensions.iec61970.base.feeder.lv_feeder import LvFeeder
    from zepben.ewb.model.cim.iec61970.base.core.equipment import Equipment
    from zepben.ewb.model.cim.iec61970.base.core.substation import Substation
    from zepben.ewb.model.cim.iec61970.base.core.terminal import Terminal


@dataslot
@boilermaker
class Feeder(EquipmentContainer):
    """
    A collection of equipment for organizational purposes, used for grouping distribution resources.
    The organization of a feeder does not necessarily reflect connectivity or current operation state.
    """

    normal_head_terminal: Terminal | None = ValidatedDescriptor(None)
    """The normal head terminal or terminals of the feeder."""

    normal_energizing_substation: Substation | None = None
    """The substation that nominally energizes the feeder. Also used for naming purposes."""

    current_equipment: List[Equipment] | None = MRIDDictAccessor()
    """The equipment contained in this feeder in the current state of the network."""

    normal_energized_lv_feeders: List[LvFeeder] | None = MRIDDictAccessor()
    """The LV feeders that are energized by this feeder in the normal state of the network."""

    current_energized_lv_feeders: List[LvFeeder] | None = MRIDDictAccessor()
    """The LV feeders that are energized by this feeder in the current state of the network."""

    def _retype(self):
        self.current_equipment: MRIDDictRouter = ...
        self.normal_energized_lv_feeders: MRIDDictRouter = ...
        self.current_energized_lv_feeders: MRIDDictRouter = ...

    @validate(normal_head_terminal)
    def _normal_head_terminal_validate(self, term: Terminal | None):
        if self.normal_head_terminal is None or self.normal_head_terminal is term or (self.num_equipment() == 0 and self.num_current_equipment() == 0):
            return term
        else:
            raise ValueError(f"Feeder {self.mrid} has equipment assigned to it. Cannot update normalHeadTerminal on a feeder with equipment assigned.")

    @deprecated("BOILERPLATE: Use len(current_equipment) instead")
    def num_current_equipment(self):
        return len(self.current_equipment)

    @deprecated("BOILERPLATE: Use current_equipment.get_by_mrid(mrid) instead")
    def get_current_equipment(self, mrid: str) -> Equipment:
        """
        Get the `Equipment` for this `Feeder` identified by `mrid`

        `mrid` The mRID of the required `Equipment`
        Returns The `Equipment` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return self.current_equipment.get_by_mrid(mrid)

    @deprecated("BOILERPLATE: Use current_equipment.append(equipment) instead")
    def add_current_equipment(self, equipment: Equipment) -> Feeder:
        """
        Associate `equipment` with this `Feeder`.

        `equipment` the `Equipment` to associate with this `Feeder`.
        Returns A reference to this `Feeder` to allow fluent use.
        Raises `ValueError` if another `Equipment` with the same `mrid` already exists for this `Feeder`.
        """
        self.current_equipment.append(equipment)
        return self

    @deprecated("BOILERPLATE: Use current_equipment.remove(equipment) instead")
    def remove_current_equipment(self, equipment: Equipment) -> Feeder:
        return self.current_equipment.remove(equipment)

    @deprecated("BOILERPLATE: Use current_equipment.clear() instead")
    def clear_current_equipment(self) -> Feeder:
        return self.current_equipment.clear()

    @deprecated("BOILERPLATE: Use len(normal_energized_lv_feeders) instead")
    def num_normal_energized_lv_feeders(self) -> int:
        return len(self.normal_energized_lv_feeders)

    @deprecated("BOILERPLATE: Use normal_energized_lv_feeders.get_by_mrid(mrid) instead")
    def get_normal_energized_lv_feeder(self, mrid: str) -> LvFeeder:
        """
        Energized LvFeeder in the normal state of the network.

        @param mrid: The mrid of the `LvFeeder`.
        @return A matching `LvFeeder` that is energized by this `Feeder` in the normal state of the network.
        @raise A `KeyError` if no matching `LvFeeder` was found.
        """
        return self.normal_energized_lv_feeders.get_by_mrid(mrid)

    @deprecated("BOILERPLATE: Use normal_energized_lv_feeders.append(lv_feeder) instead")
    def add_normal_energized_lv_feeder(self, lv_feeder: LvFeeder) -> Feeder:
        """
        Associate this `Feeder` with an `LvFeeder` in the normal state of the network.

        @param lv_feeder: the LV feeder to associate with this feeder in the normal state of the network.
        @return: This `Feeder` for fluent use.
        """
        self.normal_energized_lv_feeders.append(lv_feeder)
        return self

    @deprecated("BOILERPLATE: Use normal_energized_lv_feeders.remove(lv_feeder) instead")
    def remove_normal_energized_lv_feeder(self, lv_feeder: LvFeeder) -> Feeder:
        return self.normal_energized_lv_feeders.remove(lv_feeder)

    @deprecated("BOILERPLATE: Use normal_energized_lv_feeders.clear() instead")
    def clear_normal_energized_lv_feeders(self) -> Feeder:
        return self.normal_energized_lv_feeders.clear()

    @deprecated("BOILERPLATE: Use len(current_energized_lv_feeders) instead")
    def num_current_energized_lv_feeders(self) -> int:
        return len(self.current_energized_lv_feeders)

    @deprecated("BOILERPLATE: Use current_energized_lv_feeders.get_by_mrid(mrid) instead")
    def get_current_energized_lv_feeder(self, mrid: str) -> LvFeeder:
        """
        Energized LvFeeder in the current state of the network.

        @param mrid: The mrid of the `LvFeeder`.
        @return A matching `LvFeeder` that is energized by this `Feeder` in the current state of the network.
        @raise A `KeyError` if no matching `LvFeeder` was found.
        """
        return self.current_energized_lv_feeders.get_by_mrid(mrid)

    @deprecated("BOILERPLATE: Use current_energized_lv_feeders.append(lv_feeder) instead")
    def add_current_energized_lv_feeder(self, lv_feeder: LvFeeder) -> Feeder:
        """
        Associate this `Feeder` with an `LvFeeder` in the current state of the network.

        @param lv_feeder: the LV feeder to associate with this feeder in the current state of the network.
        @return: This `Feeder` for fluent use.
        """
        self.current_energized_lv_feeders.append(lv_feeder)
        return self

    @deprecated("BOILERPLATE: Use current_energized_lv_feeders.remove(lv_feeder) instead")
    def remove_current_energized_lv_feeder(self, lv_feeder: LvFeeder) -> Feeder:
        return self.current_energized_lv_feeders.remove(lv_feeder)

    @deprecated("BOILERPLATE: Use current_energized_lv_feeders.clear() instead")
    def clear_current_energized_lv_feeders(self) -> Feeder:
        self.current_energized_lv_feeders.clear()
        return self

