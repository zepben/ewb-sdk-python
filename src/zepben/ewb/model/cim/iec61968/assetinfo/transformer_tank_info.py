#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["TransformerTankInfo"]

from typing import Optional, List, Generator, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61968.assets.asset_info import AssetInfo
from zepben.ewb.model.resistance_reactance import ResistanceReactance
from zepben.ewb.util import nlen, ngen, safe_remove, get_by_mrid

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.assetinfo.power_transformer_info import PowerTransformerInfo
    from zepben.ewb.model.cim.iec61968.assetinfo.transformer_end_info import TransformerEndInfo


@dataslot
@boilermaker
class TransformerTankInfo(AssetInfo):
    """Set of transformer tank data, from an equipment library."""

    power_transformer_info: PowerTransformerInfo | None = None
    """Power transformer data that this tank description is part of."""

    transformer_end_infos: List[TransformerEndInfo] | None = MRIDListAccessor()
    """Data for all the ends described by this transformer tank data."""

    def _retype(self):
        self.transformer_end_infos: MRIDListRouter = ...
    
    @deprecated("BOILERPLATE: Use len(transformer_end_infos) instead")
    def num_transformer_end_infos(self):
        return len(self.transformer_end_infos)

    @deprecated("BOILERPLATE: Use transformer_end_infos.get_by_mrid(mrid) instead")
    def get_transformer_end_info(self, mrid: str) -> TransformerEndInfo:
        return self.transformer_end_infos.get_by_mrid(mrid)

    @deprecated("BOILERPLATE: Use transformer_end_infos.append(tei) instead")
    def add_transformer_end_info(self, tei: TransformerEndInfo) -> TransformerTankInfo:
        return self.transformer_end_infos.append(tei)

    @deprecated("BOILERPLATE: Use transformer_end_infos.remove(tei) instead")
    def remove_transformer_end_info(self, tei: TransformerEndInfo) -> TransformerTankInfo:
        return self.transformer_end_infos.remove(tei)

    @deprecated("BOILERPLATE: Use transformer_end_infos.clear() instead")
    def clear_transformer_end_infos(self) -> TransformerTankInfo:
        return self.transformer_end_infos.clear()

    def resistance_reactance(self, end_number: int) -> ResistanceReactance | None:
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
