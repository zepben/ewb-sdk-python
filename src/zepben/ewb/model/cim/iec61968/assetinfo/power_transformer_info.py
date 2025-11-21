#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["PowerTransformerInfo"]

from typing import List, Optional, Generator, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61968.assets.asset_info import AssetInfo
from zepben.ewb.model.resistance_reactance import ResistanceReactance
from zepben.ewb.util import nlen, ngen, get_by_mrid, safe_remove

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.assetinfo.transformer_tank_info import TransformerTankInfo


@dataslot
@boilermaker
class PowerTransformerInfo(AssetInfo):
    """Set of power transformer data, from an equipment library."""

    transformer_tank_infos: List[TransformerTankInfo] | None = MRIDListAccessor()
    """Data for all the tanks described by this power transformer data."""

    def _retype(self):
        self.transformer_tank_infos: MRIDListRouter[TransformerTankInfo] = ...
    
    @deprecated("BOILERPLATE: Use len(transformer_tank_infos) instead")
    def num_transformer_tank_infos(self):
        return len(self.transformer_tank_infos)

    @deprecated("BOILERPLATE: Use transformer_tank_infos.get_by_mrid(mrid) instead")
    def get_transformer_tank_info(self, mrid: str) -> TransformerTankInfo:
        return self.transformer_tank_infos.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use transformer_tank_infos.append(tti) instead")
    def add_transformer_tank_info(self, tti: TransformerTankInfo) -> PowerTransformerInfo:
        self.transformer_tank_infos.append(tti)
        return self

    @deprecated("Boilerplate: Use transformer_tank_infos.remove(tti) instead")
    def remove_transformer_tank_info(self, tti: TransformerTankInfo) -> PowerTransformerInfo:
        self.transformer_tank_infos.remove(tti)
        return self

    @deprecated("BOILERPLATE: Use transformer_tank_infos.clear() instead")
    def clear_transformer_tank_infos(self) -> PowerTransformerInfo:
        return self.transformer_tank_infos.clear()

    def resistance_reactance(self, end_number: int) -> ResistanceReactance | None:
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
