#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["LvFeeder"]

import typing
from dataclasses import field
from typing import Optional, Dict

from typing_extensions import deprecated

from zepben.ewb.boilerplate.collections.mrid_collection import MridCollection
from zepben.ewb.boilerplate.collections.mrid_map import LazyMridMap
from zepben.ewb.model.cim.extensions.zbex import zbex
from zepben.ewb.model.cim.iec61970.base.core.equipment_container import EquipmentContainer
from zepben.ewb.boilerplate.dataclass_base import zb_dataclass

if typing.TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.equipment import Equipment
    from zepben.ewb.model.cim.iec61970.base.core.feeder import Feeder
    from zepben.ewb.model.cim.iec61970.base.core.terminal import Terminal


@zb_dataclass
@zbex
class LvFeeder(EquipmentContainer):
    """
    [ZBEX]
    A branch of LV network starting at a distribution substation and continuing until the end of the LV network.

    :var normal_head_terminal: [ZBEX] The normal head terminal or terminals of this LvFeeder
    :var normal_energizing_feeders: [ZBEX] The feeders that energize this LvFeeder in the normal state of the network.
    :var current_equipment: [ZBEX] The equipment contained in this LvFeeder in the current state of the network.
    :var current_energizing_feeders: [ZBEX] The feeders that energize this LvFeeder in the current state of the network.
    :var normal_energizing_lv_substation: [ZBEX] The normally energizing LvSubstation for this LvFeeder

    """

    _normal_head_terminal: Terminal | None = None
    """[ZBEX] The normal head terminal or terminals of this LvFeeder"""

    _normal_energizing_feeders_by_id: Dict[str, Feeder] | None = field(default=None)
    """[ZBEX] The feeders that energize this LV feeder in the normal state of the network."""

    _current_equipment_by_id: Dict[str, Equipment] | None = field(default=None)
    """[ZBEX] The equipment contained in this LvFeeder in the current state of the network."""

    _current_energizing_feeders_by_id: Dict[str, Feeder] | None = field(default=None)
    """[ZBEX] The feeders that energize this LV feeder in the current state of the network."""

    normal_energizing_lv_substation: 'LvSubstation | None' = None
    """[ZBEX] The normally energizing LvSubstation for this LvFeeder"""

    current_equipment: MridCollection[Equipment] = LazyMridMap(
        _current_equipment_by_id,
        "A current Equipment",
    )
    """Contained `Equipment` using the current state of the network."""

    normal_energizing_feeders: MridCollection[Feeder] = LazyMridMap(
        _normal_energizing_feeders_by_id,
        "A Feeder",
    )
    """[ZBEX] The HV/MV feeders that normally energize this LV feeder."""

    current_energizing_feeders: MridCollection[Feeder] = LazyMridMap(
        _current_energizing_feeders_by_id,
        "A Feeder",
    )
    """[ZBEX] The HV/MV feeders that currently energize this LV feeder."""

    @property
    def normal_head_terminal(self) -> Optional[Terminal]:
        """
        [ZBEX] The normal head terminal or terminals of the feeder.
        """
        return self._normal_head_terminal

    @normal_head_terminal.setter
    def normal_head_terminal(self, term: Optional[Terminal]):
        if self._normal_head_terminal is None or self._normal_head_terminal is term:
            self._normal_head_terminal = term
        else:
            raise ValueError(f"normal_head_terminal for {str(self)} has already been set to {self._normal_head_terminal}, cannot reset this field to {term}")


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
    # region normal_energizing_feeders boilerplate

    @deprecated("Use len(normal_energizing_feeders) instead")
    def num_normal_energizing_feeders(self):
        return len(self.normal_energizing_feeders)

    @deprecated("Use normal_energizing_feeders.get_by_mrid(mrid) instead")
    def get_normal_energizing_feeder(self, mrid: str) -> Feeder:
        return self.normal_energizing_feeders.get_by_mrid(mrid)

    @deprecated("Use normal_energizing_feeders.append(lv_feeder) instead")
    def add_normal_energizing_feeder(self, lv_feeder: Feeder) -> LvFeeder:
        self.normal_energizing_feeders.append(lv_feeder)
        return self

    @deprecated("Use normal_energizing_feeders.remove(lv_feeder) instead")
    def remove_normal_energizing_feeder(self, lv_feeder: Feeder) -> LvFeeder:
        self.normal_energizing_feeders.remove(lv_feeder)
        return self

    @deprecated("Use normal_energizing_feeders.clear() instead")
    def clear_normal_energizing_feeders(self) -> LvFeeder:
        self.normal_energizing_feeders.clear()
        return self

    # endregion
    # region current_energizing_feeders boilerplate

    @deprecated("Use len(current_energizing_feeders) instead")
    def num_current_energizing_feeders(self):
        return len(self.current_energizing_feeders)

    @deprecated("Use current_energizing_feeders.get_by_mrid(mrid) instead")
    def get_current_energizing_feeder(self, mrid: str) -> Feeder:
        return self.current_energizing_feeders.get_by_mrid(mrid)

    @deprecated("Use current_energizing_feeders.append(lv_feeder) instead")
    def add_current_energizing_feeder(self, lv_feeder: Feeder) -> LvFeeder:
        self.current_energizing_feeders.append(lv_feeder)
        return self

    @deprecated("Use current_energizing_feeders.remove(lv_feeder) instead")
    def remove_current_energizing_feeder(self, lv_feeder: Feeder) -> LvFeeder:
        self.current_energizing_feeders.remove(lv_feeder)
        return self

    @deprecated("Use current_energizing_feeders.clear() instead")
    def clear_current_energizing_feeders(self) -> LvFeeder:
        self.current_energizing_feeders.clear()
        return self

    # endregion
    # endregion
