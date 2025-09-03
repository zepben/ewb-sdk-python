#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["GeographicalRegion"]

from typing import Optional, List

from zepben.ewb.collections.autoslot import autoslot_dataclass
from zepben.ewb.collections.mrid_list import MRIDList
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.model.cim.iec61970.base.core.sub_geographical_region import SubGeographicalRegion


@autoslot_dataclass
class GeographicalRegion(IdentifiedObject):
    """
    A geographical region of a power system network phases.
    """
    sub_geographical_regions: Optional[List[SubGeographicalRegion]] = None

    def __post_init__(self):
        self.sub_geographical_regions: MRIDList[SubGeographicalRegion] = MRIDList(self.sub_geographical_regions)

    def num_sub_geographical_regions(self) -> int:
        """
        Returns The number of `SubGeographicalRegion`s associated with this `GeographicalRegion`
        """
        return len(self.sub_geographical_regions)

    def get_sub_geographical_region(self, mrid: str) -> SubGeographicalRegion:
        """
        Get the `SubGeographicalRegion` for this `GeographicalRegion` identified by `mrid`

        `mrid` The mRID of the required `SubGeographicalRegion`
        Returns The `SubGeographicalRegion` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return self.sub_geographical_regions.get_by_mrid(mrid)

    def add_sub_geographical_region(self, sub_geographical_region: SubGeographicalRegion) -> GeographicalRegion:
        """
        Associate a `SubGeographicalRegion` with this `GeographicalRegion`

        `sub_geographical_region` The `SubGeographicalRegion` to associate with this `GeographicalRegion`.
        Returns A reference to this `GeographicalRegion` to allow fluent use.
        Raises `ValueError` if another `SubGeographicalRegion` with the same `mrid` already exists for this `GeographicalRegion`.
        """
        self.sub_geographical_regions.add(sub_geographical_region)
        return self

    def remove_sub_geographical_region(self, sub_geographical_region: SubGeographicalRegion) -> GeographicalRegion:
        """
        Disassociate `sub_geographical_region` from this `GeographicalRegion`
        `sub_geographical_region` The `SubGeographicalRegion` to disassociate from this `GeographicalRegion`.
        Returns A reference to this `GeographicalRegion` to allow fluent use.
        Raises `ValueError` if `sub_geographical_region` was not associated with this `GeographicalRegion`.
        """
        self.sub_geographical_regions.remove(sub_geographical_region)
        return self

    def clear_sub_geographical_regions(self) -> GeographicalRegion:
        """
        Clear all SubGeographicalRegions.
        Returns A reference to this `GeographicalRegion` to allow fluent use.
        """
        self.sub_geographical_regions.clear()
        return self
