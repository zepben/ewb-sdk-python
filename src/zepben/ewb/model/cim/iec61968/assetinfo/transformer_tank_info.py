#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["TransformerTankInfo"]

from typing import Optional, List, TYPE_CHECKING
from dataclasses import field
from typing_extensions import deprecated

from zepben.ewb.model.cim.iec61968.assets.asset_info import AssetInfo
from zepben.ewb.model.resistance_reactance import ResistanceReactance
from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb.boilerplate.collections.mrid_list import LazyMridList
from zepben.ewb.boilerplate.collections.mrid_collection import MridCollection

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.assetinfo.power_transformer_info import PowerTransformerInfo
    from zepben.ewb.model.cim.iec61968.assetinfo.transformer_end_info import TransformerEndInfo


@zb_dataclass
class TransformerTankInfo(AssetInfo):
    """Set of transformer tank data, from an equipment library."""

    power_transformer_info: Optional[PowerTransformerInfo] = None
    """Power transformer data that this tank description is part of."""

    _transformer_end_infos: Optional[List[TransformerEndInfo]] = field(default=None)
    """Data for all the ends described by this transformer tank data."""

    transformer_end_infos: MridCollection[TransformerEndInfo] = LazyMridList(
        _transformer_end_infos,
        "A TransformerEndInfo",
    )


    def resistance_reactance(self, end_number: int) -> Optional[ResistanceReactance]:
        """
        Get the `ResistanceReactance` for the specified `end_number` from the datasheet information.
        `end_number` The number of the end to fetch the ResistanceReactance for.
        Returns a `ResistanceReactance` for the specified end, or None if one couldn't be calculated.
        """
        for tei in self.transformer_end_infos:
            if tei.end_number == end_number:
                rr = tei.resistance_reactance()
                if rr is not None:
                    return rr
        else:
            return None

    # region deprecated list boilerplate
    # region transformer_end_infos boilerplate

    @deprecated("Use len(obj.transformer_end_infos) instead.")
    def num_transformer_end_infos(self):
        return len(self.transformer_end_infos)

    @deprecated("Use obj.transformer_end_infos.get_by_mrid(mrid) instead.")
    def get_transformer_end_info(self, mrid: str) -> TransformerEndInfo:
        return self.transformer_end_infos.get_by_mrid(mrid)

    @deprecated("Use obj.transformer_end_infos.append(tei) instead.")
    def add_transformer_end_info(self, tei: TransformerEndInfo) -> TransformerTankInfo:
        self.transformer_end_infos.append(tei)
        return self

    @deprecated("Use obj.transformer_end_infos.remove(tei) instead.")
    def remove_transformer_end_info(self, tei: TransformerEndInfo) -> TransformerTankInfo:
        self.transformer_end_infos.remove(tei)
        return self

    @deprecated("Use obj.transformer_end_infos.clear() instead.")
    def clear_transformer_end_infos(self) -> TransformerTankInfo:
        self.transformer_end_infos.clear()
        return self

    # endregion transformer_end_infos boilerplate

    # endregion deprecated list boilerplate
