#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["GeographicalRegion"]

from typing import Optional, List, Generator

from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.model.cim.iec61970.base.core.sub_geographical_region import SubGeographicalRegion
from zepben.ewb.util import nlen, ngen, get_by_mrid, safe_remove


class GeographicalRegion(IdentifiedObject):
    """
    A geographical region of a power system network phases.
    """
    _sub_geographical_regions: Optional[List[SubGeographicalRegion]] = None

    def __init__(self, sub_geographical_regions: List[SubGeographicalRegion] = None, **kwargs):
        super(GeographicalRegion, self).__init__(**kwargs)
        if sub_geographical_regions:
            for sgr in sub_geographical_regions:
                self.add_sub_geographical_region(sgr)

    def num_sub_geographical_regions(self) -> int:
        """
        Returns The number of `SubGeographicalRegion`s associated with this `GeographicalRegion`
        """
        return nlen(self._sub_geographical_regions)

    @property
    def sub_geographical_regions(self) -> Generator[SubGeographicalRegion, None, None]:
        """
        The `SubGeographicalRegion`s of this `GeographicalRegion`.
        """
        return ngen(self._sub_geographical_regions)

    def get_sub_geographical_region(self, mrid: str) -> SubGeographicalRegion:
        """
        Get the `SubGeographicalRegion` for this `GeographicalRegion` identified by `mrid`

        `mrid` The mRID of the required `SubGeographicalRegion`
        Returns The `SubGeographicalRegion` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._sub_geographical_regions, mrid)

    def add_sub_geographical_region(self, sub_geographical_region: SubGeographicalRegion) -> GeographicalRegion:
        """
        Associate a `SubGeographicalRegion` with this `GeographicalRegion`

        `sub_geographical_region` The `SubGeographicalRegion` to associate with this `GeographicalRegion`.
        Returns A reference to this `GeographicalRegion` to allow fluent use.
        Raises `ValueError` if another `SubGeographicalRegion` with the same `mrid` already exists for this `GeographicalRegion`.
        """
        if self._validate_reference(sub_geographical_region, self.get_sub_geographical_region, "A SubGeographicalRegion"):
            return self
        self._sub_geographical_regions = list() if self._sub_geographical_regions is None else self._sub_geographical_regions
        self._sub_geographical_regions.append(sub_geographical_region)
        return self

    def remove_sub_geographical_region(self, sub_geographical_region: SubGeographicalRegion) -> GeographicalRegion:
        """
        Disassociate `sub_geographical_region` from this `GeographicalRegion`
        `sub_geographical_region` The `SubGeographicalRegion` to disassociate from this `GeographicalRegion`.
        Returns A reference to this `GeographicalRegion` to allow fluent use.
        Raises `ValueError` if `sub_geographical_region` was not associated with this `GeographicalRegion`.
        """
        self._sub_geographical_regions = safe_remove(self._sub_geographical_regions, sub_geographical_region)
        return self

    def clear_sub_geographical_regions(self) -> GeographicalRegion:
        """
        Clear all SubGeographicalRegions.
        Returns A reference to this `GeographicalRegion` to allow fluent use.
        """
        self._sub_geographical_regions = None
        return self
