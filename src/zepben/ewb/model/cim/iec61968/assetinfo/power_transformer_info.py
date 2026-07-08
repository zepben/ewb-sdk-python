#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["PowerTransformerInfo"]

from typing import List, Optional, Generator, TYPE_CHECKING
from dataclasses import field
from typing_extensions import deprecated

from zepben.ewb.model.cim.iec61968.assets.asset_info import AssetInfo
from zepben.ewb.model.resistance_reactance import ResistanceReactance
from zepben.ewb.util import nlen, ngen, get_by_mrid, safe_remove
from zepben.ewb.dataclass_descriptors.dataclass_base import zb_dataclass
from zepben.ewb import remove_descriptor_annotations
from zepben.ewb.dataclass_descriptors.mrid_list import MridCollection, LazyMridList

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.assetinfo.transformer_tank_info import TransformerTankInfo


@zb_dataclass
class PowerTransformerInfo(AssetInfo):
    """Set of power transformer data, from an equipment library."""

    _transformer_tank_infos: Optional[List[TransformerTankInfo]] = field(default=None)
    """Data for all the tanks described by this power transformer data."""

    transformer_tank_infos: MridCollection[TransformerTankInfo] = LazyMridList(
        _transformer_tank_infos,
        "A TransformerTankInfo",
    )


    def resistance_reactance(self, end_number: int) -> Optional[ResistanceReactance]:
        """
        Get the `ResistanceReactance` for the specified `end_number` from the datasheet information.
        `end_number` The number of the end to fetch the ResistanceReactance for.
        Returns a `ResistanceReactance` for the specified end, or None if one couldn't be calculated.
        """
        for tti in self.transformer_tank_infos:
            rr = tti.resistance_reactance(end_number)
            if rr is not None:
                return rr
        else:
            return None

    # region deprecated list boilerplate
    # region transformer_tank_infos boilerplate

    @deprecated("Use len(obj.transformer_tank_infos) instead.")
    def num_transformer_tank_infos(self):
        return len(self.transformer_tank_infos)

    @deprecated("Use obj.transformer_tank_infos.get_by_mrid(mrid) instead.")
    def get_transformer_tank_info(self, mrid: str) -> TransformerTankInfo:
        return self.transformer_tank_infos.get_by_mrid(mrid)

    @deprecated("Use obj.transformer_tank_infos.append(tti) instead.")
    def add_transformer_tank_info(self, tti: TransformerTankInfo) -> PowerTransformerInfo:
        self.transformer_tank_infos.append(tti)
        return self

    @deprecated("Use obj.transformer_tank_infos.remove(tti) instead.")
    def remove_transformer_tank_info(self, tti: TransformerTankInfo) -> PowerTransformerInfo:
        self.transformer_tank_infos.remove(tti)
        return self

    @deprecated("Use obj.transformer_tank_infos.clear() instead.")
    def clear_transformer_tank_infos(self) -> PowerTransformerInfo:
        self.transformer_tank_infos.clear()
        return self

    # endregion transformer_tank_infos boilerplate

    # endregion deprecated list boilerplate
