#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ['LvSubstation']

from dataclasses import field
from typing import Generator, TYPE_CHECKING

from typing_extensions import deprecated

from zepben.ewb.boilerplate.collections.mrid_collection import MridCollection
from zepben.ewb.boilerplate.collections.mrid_map import LazyMridMap
from zepben.ewb.model.cim.extensions.zbex import zbex
from zepben.ewb.model.cim.iec61970.base.core.equipment_container import EquipmentContainer
from zepben.ewb.model.cim.extensions.iec61970.base.feeder.lv_feeder import LvFeeder
from zepben.ewb.boilerplate.dataclass_base import zb_dataclass

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.feeder import Feeder


@zb_dataclass
@zbex
class LvSubstation(EquipmentContainer):
    """
    [ZBEX] a collection of equipment for purposes other than generation or utilization, through which electric energy in bulk is passed for the distribution of
    energy to low voltage network.
    :var normal_energizing_feeders: [ZBEX] the feeders that normally energize the substation. also used for naming purposes.
    :var normal_energized_lv_feeders: [ZBEX] the lv_feeders that are normally energized by this lv_substation. also used for naming purposes.
    :var current_energizing_feeders: [ZBEX] the feeders that currently energize the substation. also used for naming purposes.
    """

    _normal_energizing_feeders_by_id: dict[str | None, 'Feeder'] | None = field(default=None)
    _current_energizing_feeders_by_id: dict[str | None, 'Feeder'] | None = field(default=None)
    _normal_energized_lv_feeders_by_id: dict[str | None, LvFeeder] | None = field(default=None)

    normal_energizing_feeders: MridCollection[Feeder] = LazyMridMap(
        _normal_energizing_feeders_by_id,
        "A Feeder",
    )
    """[ZBEX] The HV/MV feeders that normally energize this ``LvSubstation``."""

    normal_energized_lv_feeders: MridCollection[LvFeeder] = LazyMridMap(
        _normal_energized_lv_feeders_by_id,
        "An LvFeeder",
    )
    """[ZBEX] the ``LvFeeders`` that are normally energized by this ``LvSubstation``."""

    current_energizing_feeders: MridCollection[Feeder] = LazyMridMap(
        _current_energizing_feeders_by_id,
        "A Feeder",
    )
    """[ZBEX] The HV/MV feeders that currently energize this LV substation."""

    def normal_energized_lv_switch_feeders(self) -> Generator[LvFeeder, None, None]:
        """
        Retrieves all normally energized LvFeeders that represent low voltage network connected below a switch on the edge of this LvSubstation. This is all
        LvFeeders in the normalEnergizedLvFeeders that has a normalHeadTerminal attached to a Switch.
        """
        # NOTE: import exists here due to a circular import problem
        from zepben.ewb.model.cim.iec61970.base.wires.switch import Switch

        for lv_feeder in self.normal_energized_lv_feeders:
            if (it := lv_feeder.normal_head_terminal) is not None and isinstance(it.conducting_equipment, Switch):
                yield lv_feeder


    # region deprecated list boilerplate
    # region normal_energizing_feeders boilerplate

    @deprecated("Use len(normal_energizing_feeders) instead")
    def num_normal_energizing_feeders(self):
        return len(self.normal_energizing_feeders)

    @deprecated("Use normal_energizing_feeders.get_by_mrid(mrid) instead")
    def get_normal_energizing_feeder(self, mrid: str) -> Feeder:
        return self.normal_energizing_feeders.get_by_mrid(mrid)

    @deprecated("Use normal_energizing_feeders.append(lv_feeder) instead")
    def add_normal_energizing_feeder(self, lv_feeder: Feeder) -> LvSubstation:
        self.normal_energizing_feeders.append(lv_feeder)
        return self

    @deprecated("Use normal_energizing_feeders.remove(lv_feeder) instead")
    def remove_normal_energizing_feeder(self, lv_feeder: Feeder) -> LvSubstation:
        self.normal_energizing_feeders.remove(lv_feeder)
        return self

    @deprecated("Use normal_energizing_feeders.clear() instead")
    def clear_normal_energizing_feeders(self) -> LvSubstation:
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
    def add_current_energizing_feeder(self, lv_feeder: Feeder) -> LvSubstation:
        self.current_energizing_feeders.append(lv_feeder)
        return self

    @deprecated("Use current_energizing_feeders.remove(lv_feeder) instead")
    def remove_current_energizing_feeder(self, lv_feeder: Feeder) -> LvSubstation:
        self.current_energizing_feeders.remove(lv_feeder)
        return self

    @deprecated("Use current_energizing_feeders.clear() instead")
    def clear_current_energizing_feeders(self) -> LvSubstation:
        self.current_energizing_feeders.clear()
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
    def add_normal_energized_lv_feeder(self, lv_feeder: LvFeeder) -> LvSubstation:
        self.normal_energized_lv_feeders.append(lv_feeder)
        return self

    @deprecated("Use normal_energized_lv_feeders.remove(lv_feeder) instead")
    def remove_normal_energized_lv_feeder(self, lv_feeder: LvFeeder) -> LvSubstation:
        self.normal_energized_lv_feeders.remove(lv_feeder)
        return self

    @deprecated("Use normal_energized_lv_feeders.clear() instead")
    def clear_normal_energized_lv_feeders(self) -> LvSubstation:
        self.normal_energized_lv_feeders.clear()
        return self

    # endregion
    # endregion
