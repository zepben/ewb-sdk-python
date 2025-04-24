#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional, TYPE_CHECKING, List, Generator, Iterable

if TYPE_CHECKING:
    from zepben.evolve.model.cim.iec61968.assets.asset_info import AssetInfo
    from zepben.evolve.model.cim.iec61968.common.location import Location
    from zepben.evolve import Asset

from zepben.evolve.util import get_by_mrid, nlen, ngen, safe_remove
from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject

__all__ = ['PowerSystemResource']


class PowerSystemResource(IdentifiedObject):
    """
    Abstract class, should only be used through subclasses.
    A power system resource can be an item of equipment such as a switch, an equipment container containing many individual
    items of equipment such as a substation, or an organisational entity such as sub-control area. Power system resources
    can have measurements associated.
    """

    location: Optional[Location] = None
    """A `zepben.evolve.iec61968.common.location.Location` for this resource."""

    asset_info: Optional[AssetInfo] = None
    """A subclass of `zepben.evolve.iec61968.assets.asset_info.AssetInfo` providing information about the asset associated with this PowerSystemResource."""

    num_controls: int = 0
    """Number of Control's known to associate with this [PowerSystemResource]"""

    _assets: Optional[List[Asset]] = None

    def __init__(self, assets: Iterable[Asset] = None, **kwargs):
        super(PowerSystemResource, self).__init__(**kwargs)
        if assets:
            for asset in assets:
                self.add_asset(asset)

    @property
    def has_controls(self) -> bool:
        """
        * :return: True if this [PowerSystemResource] has at least 1 Control associated with it, false otherwise.
        """
        return self.num_controls > 0

    def num_assets(self) -> int:
        """
        Get the number of `Asset`s associated with this `PowerSystemResource`.
        """
        return nlen(self._assets)

    @property
    def assets(self) -> Generator[Asset, None, None]:
        """
        The `Asset`s of this `PowerSystemResource`.
        """
        return ngen(self._assets)

    def get_asset(self, mrid: str) -> Asset:
        """
        Get the `Asset` associated with this `PowerSystemResource` identified by `mrid`.

        `mrid` the mRID of the required `Asset`
        Returns The `Asset` with the specified `mrid`.
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._assets, mrid)

    def add_asset(self, asset: Asset) -> PowerSystemResource:
        """
        `asset` The `Asset` to associate with this `PowerSystemResource`.
        Returns A reference to this `PowerSystemResource` to allow fluent use.
        Raises `ValueError` if another `Asset` with the same `mrid` already exists in this `PowerSystemResource`
        """
        if self._validate_reference(asset, self.get_asset, "An Asset"):
            return self

        self._assets = list() if self._assets is None else self._assets
        self._assets.append(asset)
        return self

    def remove_asset(self, asset: Asset) -> PowerSystemResource:
        """
        Disassociate an `Asset` from this `PowerSystemResource`.

        `asset` the `Asset` to disassociate from this `PowerSystemResource`.
        Raises `ValueError` if `asset` was not associated with this `PowerSystemResource`.
        Returns A reference to this `PowerSystemResource` to allow fluent use.
        """
        self._assets = safe_remove(self._assets, asset)
        return self

    def clear_assets(self) -> PowerSystemResource:
        """
        Clear all assets.
        Returns self
        """
        self._assets = None
        return self
