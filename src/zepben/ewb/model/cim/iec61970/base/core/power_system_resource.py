#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ['PowerSystemResource']

from typing import TYPE_CHECKING, List

from typing_extensions import deprecated

from zepben.ewb.dataslot import MRIDListRouter, dataslot, MRIDListAccessor
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.util import nlen

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.assets.asset import Asset
    from zepben.ewb.model.cim.iec61968.assets.asset_info import AssetInfo
    from zepben.ewb.model.cim.iec61968.common.location import Location


@dataslot
class PowerSystemResource(IdentifiedObject):
    """
    Abstract class, should only be used through subclasses.
    A power system resource can be an item of equipment such as a switch, an equipment container containing many individual
    items of equipment such as a substation, or an organisational entity such as sub-control area. Power system resources
    can have measurements associated.
    """

    location: Location | None = None
    """A `zepben.ewb.model.cim.iec61968.common.location.Location` for this resource."""

    asset_info: AssetInfo | None = None
    """A subclass of `zepben.ewb.model.cim.iec61968.assets.asset_info.AssetInfo` providing information about the asset associated with this PowerSystemResource."""

    num_controls: int | None = None
    """Number of Control's known to associate with this [PowerSystemResource]"""

    assets: List[Asset] | None = MRIDListAccessor()

    def _retype(self):
        self.assets: MRIDListRouter[Asset] = ...
    
    @property
    def has_controls(self) -> bool:
        """
        * :return: True if this [PowerSystemResource] has at least 1 Control associated with it, false otherwise.
        """
        return nlen(self.num_controls) > 0

    @deprecated("BOILERPLATE: Use len(assets) instead")
    def num_assets(self) -> int:
        return len(self.assets)

    @deprecated("BOILERPLATE: Use assets.get_by_mrid(mrid) instead")
    def get_asset(self, mrid: str) -> Asset:
        return self.assets.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use assets.append(asset) instead")
    def add_asset(self, asset: Asset) -> PowerSystemResource:
        self.assets.append(asset)
        return self

    @deprecated("Boilerplate: Use assets.remove(asset) instead")
    def remove_asset(self, asset: Asset) -> PowerSystemResource:
        self.assets.remove(asset)
        return self

    @deprecated("BOILERPLATE: Use assets.clear() instead")
    def clear_assets(self) -> PowerSystemResource:
        self.assets.clear()
        return self

