#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Feeder"]

from dataclasses import field
from typing import Optional, Dict, TYPE_CHECKING

from typing_extensions import deprecated

from zepben.ewb.boilerplate.collections.mrid_collection import MridCollection
from zepben.ewb.boilerplate.backfill import internal
from zepben.ewb.boilerplate.collections.mrid_map import LazyMridMap
from zepben.ewb.model.cim.iec61970.base.core.equipment_container import EquipmentContainer
from zepben.ewb.boilerplate.dataclass_base import zb_dataclass

if TYPE_CHECKING:
    from zepben.ewb.model.cim.extensions.iec61970.base.feeder.lv_substation import LvSubstation
    from zepben.ewb.model.cim.extensions.iec61970.base.feeder.lv_feeder import LvFeeder
    from zepben.ewb.model.cim.iec61970.base.core.equipment import Equipment
    from zepben.ewb.model.cim.iec61970.base.core.substation import Substation
    from zepben.ewb.model.cim.iec61970.base.core.terminal import Terminal


@zb_dataclass
class Feeder(EquipmentContainer):
    """
    A collection of equipment for organizational purposes, used for grouping distribution resources.
    The organization of a feeder does not necessarily reflect connectivity or current operation state.
    """

    _normal_head_terminal: Terminal | None = None
    """The normal head terminal or terminals of the feeder."""

    _normal_energizing_substation: Substation | None = field(default=None)

    _current_equipment_by_id: Dict[str, Equipment] | None = field(default=None)
    """The equipment contained in this feeder in the current state of the network."""

    _normal_energized_lv_feeders_by_id: Dict[str, LvFeeder] | None = field(default=None)
    """The LV feeders that are energized by this feeder in the normal state of the network."""

    _current_energized_lv_feeders_by_id: Dict[str, LvFeeder] | None = field(default=None)
    """The LV feeders that are energized by this feeder in the current state of the network."""

    _normal_energized_lv_substations_by_id: Dict[str, 'LvSubstation'] | None = field(default=None)
    _current_energized_lv_substations_by_id: Dict[str, 'LvSubstation'] | None = field(default=None)


    @property
    def normal_head_terminal(self) -> Optional[Terminal]:
        """The normal head terminal or terminals of the feeder."""
        return self._normal_head_terminal

    @normal_head_terminal.setter
    def normal_head_terminal(self, term: Optional[Terminal]):
        if self._normal_head_terminal is None or self._normal_head_terminal is term or (self.num_equipment() == 0 and self.num_current_equipment() == 0):
            self._normal_head_terminal = term
        else:
            raise ValueError(f"Feeder {self.mrid} has equipment assigned to it. Cannot update normalHeadTerminal on a feeder with equipment assigned.")

    @property
    @internal(_normal_energizing_substation)
    def normal_energizing_substation(self):
        """The substation that normally energizes the feeder. Also used for naming purposes."""
        return self._normal_energizing_substation

    @normal_energizing_substation.setter
    @deprecated("normal_energizing_substation should never be set directly - it is automatically set when adding it to the `feeders` list")
    def normal_energizing_substation(self, value):
        self._normal_energizing_substation = value

    current_equipment: MridCollection[Equipment] = LazyMridMap(
        _current_equipment_by_id,
        "A current Equipment",
    )
    """Contained `Equipment` using the current state of the network."""

    normal_energized_lv_feeders: MridCollection[LvFeeder] = LazyMridMap(
        _normal_energized_lv_feeders_by_id,
        "An LvFeeder",
    )
    """The LV feeders that are normally energized by this feeder."""

    current_energized_lv_feeders: MridCollection[LvFeeder] = LazyMridMap(
        _current_energized_lv_feeders_by_id,
        "An LvFeeder",
    )
    """[ZBEX] The LV feeders that are currently energized by this feeder."""

    normal_energized_lv_substations: MridCollection[LvSubstation] = LazyMridMap(
        _normal_energized_lv_substations_by_id,
        "An LvSubstation",
    )
    """[ZBEX]"""

    current_energized_lv_substations: MridCollection[LvSubstation] = LazyMridMap(
        _current_energized_lv_substations_by_id,
        "An LvSubstation",
    )
    """[ZBEX]"""
    # region deprecated list boilerplate
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
    # region normal_energized_lv_feeders boilerplate

    @deprecated("Use len(normal_energized_lv_feeders) instead")
    def num_normal_energized_lv_feeders(self):
        return len(self.normal_energized_lv_feeders)

    @deprecated("Use normal_energized_lv_feeders.get_by_mrid(mrid) instead")
    def get_normal_energized_lv_feeder(self, mrid: str) -> LvFeeder:
        return self.normal_energized_lv_feeders.get_by_mrid(mrid)

    @deprecated("Use normal_energized_lv_feeders.append(lv_feeder) instead")
    def add_normal_energized_lv_feeder(self, lv_feeder: LvFeeder) -> Feeder:
        self.normal_energized_lv_feeders.append(lv_feeder)
        return self

    @deprecated("Use normal_energized_lv_feeders.remove(lv_feeder) instead")
    def remove_normal_energized_lv_feeder(self, lv_feeder: LvFeeder) -> Feeder:
        self.normal_energized_lv_feeders.remove(lv_feeder)
        return self

    @deprecated("Use normal_energized_lv_feeders.clear() instead")
    def clear_normal_energized_lv_feeders(self) -> Feeder:
        self.normal_energized_lv_feeders.clear()
        return self

    # endregion
    # region current_energized_lv_feeders boilerplate

    @deprecated("Use len(current_energized_lv_feeders) instead")
    def num_current_energized_lv_feeders(self):
        return len(self.current_energized_lv_feeders)

    @deprecated("Use current_energized_lv_feeders.get_by_mrid(mrid) instead")
    def get_current_energized_lv_feeder(self, mrid: str) -> LvFeeder:
        return self.current_energized_lv_feeders.get_by_mrid(mrid)

    @deprecated("Use current_energized_lv_feeders.append(lv_feeder) instead")
    def add_current_energized_lv_feeder(self, lv_feeder: LvFeeder) -> Feeder:
        self.current_energized_lv_feeders.append(lv_feeder)
        return self

    @deprecated("Use current_energized_lv_feeders.remove(lv_feeder) instead")
    def remove_current_energized_lv_feeder(self, lv_feeder: LvFeeder) -> Feeder:
        self.current_energized_lv_feeders.remove(lv_feeder)
        return self

    @deprecated("Use current_energized_lv_feeders.clear() instead")
    def clear_current_energized_lv_feeders(self) -> Feeder:
        self.current_energized_lv_feeders.clear()
        return self

    # endregion
    # region normal_energized_lv_substations boilerplate

    @deprecated("Use len(normal_energized_lv_substations) instead")
    def num_normal_energized_lv_substations(self):
        return len(self.normal_energized_lv_substations)

    @deprecated("Use normal_energized_lv_substations.get_by_mrid(mrid) instead")
    def get_normal_energized_lv_substation(self, mrid: str) -> LvSubstation:
        return self.normal_energized_lv_substations.get_by_mrid(mrid)

    @deprecated("Use normal_energized_lv_substations.append(lv_substation) instead")
    def add_normal_energized_lv_substation(self, lv_substation: LvSubstation) -> Feeder:
        self.normal_energized_lv_substations.append(lv_substation)
        return self

    @deprecated("Use normal_energized_lv_substations.remove(lv_substation) instead")
    def remove_normal_energized_lv_substation(self, lv_substation: LvSubstation) -> Feeder:
        self.normal_energized_lv_substations.remove(lv_substation)
        return self

    @deprecated("Use normal_energized_lv_substations.clear() instead")
    def clear_normal_energized_lv_substations(self) -> Feeder:
        self.normal_energized_lv_substations.clear()
        return self

    # endregion
    # region current_energized_lv_substations boilerplate

    @deprecated("Use len(current_energized_lv_substations) instead")
    def num_current_energized_lv_substations(self):
        return len(self.current_energized_lv_substations)

    @deprecated("Use current_energized_lv_substations.get_by_mrid(mrid) instead")
    def get_current_energized_lv_substation(self, mrid: str) -> LvSubstation:
        return self.current_energized_lv_substations.get_by_mrid(mrid)

    @deprecated("Use current_energized_lv_substations.append(lv_substation) instead")
    def add_current_energized_lv_substation(self, lv_substation: LvSubstation) -> Feeder:
        self.current_energized_lv_substations.append(lv_substation)
        return self

    @deprecated("Use current_energized_lv_substations.remove(lv_substation) instead")
    def remove_current_energized_lv_substation(self, lv_substation: LvSubstation) -> Feeder:
        self.current_energized_lv_substations.remove(lv_substation)
        return self

    @deprecated("Use current_energized_lv_substations.clear() instead")
    def clear_current_energized_lv_substations(self) -> Feeder:
        self.current_energized_lv_substations.clear()
        return self

    # endregion
    # endregion
