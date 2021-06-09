#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import Optional, List, Generator

from zepben.evolve.model.cim.iec61968.assetinfo.transformer_end_info import TransformerEndInfo
from zepben.evolve.model.cim.iec61968.assets.asset_info import AssetInfo
from zepben.evolve.util import nlen, ngen, safe_remove, get_by_mrid

__all__ = ["TransformerTankInfo"]


class TransformerTankInfo(AssetInfo):
    """Set of transformer tank data, from an equipment library."""

    _transformer_end_infos: Optional[List[TransformerEndInfo]] = None
    """Data for all the ends described by this transformer tank data."""

    def __init__(self, transformer_end_infos: List[TransformerEndInfo] = None, **kwargs):
        super(TransformerTankInfo, self).__init__(**kwargs)
        if transformer_end_infos:
            for tei in transformer_end_infos:
                self.add_transformer_end_info(tei)

    def num_transformer_end_infos(self):
        """
        Get the number of `zepben.evolve.model.cim.iec61968.assetinfo.transformer_end_info.TransformerEndInfo`s associated with this `TransformerTankInfo`.
        """
        return nlen(self._transformer_end_infos)

    @property
    def transformer_end_infos(self) -> Generator[TransformerEndInfo, None, None]:
        """
        The `zepben.evolve.model.cim.iec61968.assetinfo.transformer_end_info.TransformerEndInfo`s of this `TransformerTankInfo`.
        """
        return ngen(self._transformer_end_infos)

    def get_transformer_end_info(self, mrid: str) -> TransformerEndInfo:
        """
        Get the `zepben.evolve.model.cim.iec61968.assetinfo.transformer_end_info.TransformerEndInfo` for this `TransformerTankInfo` identified by `mrid`.

        `mrid` the mRID of the required `zepben.evolve.model.cim.iec61968.assetinfo.transformer_end_info.TransformerEndInfo`
        Returns The `zepben.evolve.model.cim.iec61968.assetinfo.transformer_end_info.TransformerEndInfo` with the specified `mrid`.
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._transformer_end_infos, mrid)

    def add_transformer_end_info(self, tei: TransformerEndInfo) -> TransformerTankInfo:
        """
        `tei` The `zepben.evolve.model.cim.iec61968.assetinfo.transformer_end_info.TransformerEndInfo` to
        associate with this `TransformerTankInfo`.

        Returns A reference to this `TransformerTankInfo` to allow fluent use.

        Raises `ValueError` if another `zepben.evolve.model.cim.iec61968.assetinfo.transformer_end_info.TransformerEndInfo` with the same `mrid` already
        exists in this `TransformerTankInfo`
        """
        if self._validate_reference(tei, self.get_transformer_end_info, "A TransformerEndInfo"):
            return self

        self._transformer_end_infos = list() if self._transformer_end_infos is None else self._transformer_end_infos
        self._transformer_end_infos.append(tei)
        return self

    def remove_transformer_end_info(self, tei: TransformerEndInfo) -> TransformerTankInfo:
        """
        Disassociate an `zepben.evolve.model.cim.iec61968.assetinfo.transformer_end_info.TransformerEndInfo` from this `TransformerTankInfo`.

        `tei` the `zepben.evolve.model.cim.iec61968.assetinfo.transformer_end_info.TransformerEndInfo` to
        disassociate with this `TransformerTankInfo`.
        Raises `ValueError` if `tei` was not associated with this `TransformerTankInfo`.
        Returns A reference to this `TransformerTankInfo` to allow fluent use.
        """
        self._transformer_end_infos = safe_remove(self._transformer_end_infos, tei)
        return self

    def clear_transformer_end_infos(self) -> TransformerTankInfo:
        """
        Clears all `zepben.evolve.model.cim.iec61968.assetinfo.transformer_end_info.TransformerEndInfo`.
        Returns self
        """
        self._transformer_end_infos = None
        return self
