#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["GeographicalRegion"]

from typing import Optional, List, Generator
from dataclasses import field
from typing_extensions import deprecated

from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.model.cim.iec61970.base.core.sub_geographical_region import SubGeographicalRegion
from zepben.ewb.util import nlen, ngen, get_by_mrid, safe_remove, require
from zepben.ewb.dataclass_descriptors.dataclass_base import zb_dataclass
from zepben.ewb import remove_descriptor_annotations
from zepben.ewb.dataclass_descriptors.mrid_list import MridCollection, LazyMridList


@zb_dataclass
class GeographicalRegion(IdentifiedObject):
    """
    A geographical region of a power system network phases.
    """
    _sub_geographical_regions: Optional[List[SubGeographicalRegion]] = field(default=None)

    def __init__(self, *args, sub_geographical_regions: List[SubGeographicalRegion] = None, **kwargs):
        super(GeographicalRegion, self).__init__(*args, **kwargs)
        if sub_geographical_regions:
            for sgr in sub_geographical_regions:
                self.add_sub_geographical_region(sgr)


    sub_geographical_regions: MridCollection[SubGeographicalRegion] = LazyMridList(
        _sub_geographical_regions,
        "A SubGeographicalRegion",
    )


    def add_sub_geographical_region(self, sub_geographical_region: SubGeographicalRegion) -> GeographicalRegion:
        """
        Associate a `SubGeographicalRegion` with this `GeographicalRegion`

        `sub_geographical_region` The `SubGeographicalRegion` to associate with this `GeographicalRegion`.
        Returns A reference to this `GeographicalRegion` to allow fluent use.
        Raises `ValueError` if another `SubGeographicalRegion` with the same `mrid` already exists for this `GeographicalRegion`, or if
        `sub_geographical_region.geographical_region` is not this `GeographicalRegion`.
        """
        if self._validate_reference(sub_geographical_region, self.get_sub_geographical_region, "A SubGeographicalRegion"):
            return self

        if sub_geographical_region.geographical_region is None:
            sub_geographical_region.geographical_region = self

        require(sub_geographical_region.geographical_region is self, lambda: f"{sub_geographical_region} `geographical_region` property references " +
                                                                             f"{sub_geographical_region.geographical_region}, expected {self}.")

        self._sub_geographical_regions = list() if self._sub_geographical_regions is None else self._sub_geographical_regions
        self._sub_geographical_regions.append(sub_geographical_region)
        return self



    # region deprecated list boilerplate
    # region sub_geographical_regions boilerplate

    @deprecated("Use len(obj.sub_geographical_regions) instead.")
    def num_sub_geographical_regions(self) -> int:
        return len(self.sub_geographical_regions)

    @deprecated("Use obj.sub_geographical_regions.get_by_mrid(mrid) instead.")
    def get_sub_geographical_region(self, mrid: str) -> SubGeographicalRegion:
        return self.sub_geographical_regions.get_by_mrid(mrid)

    @deprecated("Use obj.sub_geographical_regions.remove(sub_geographical_region) instead.")
    def remove_sub_geographical_region(self, sub_geographical_region: SubGeographicalRegion) -> GeographicalRegion:
        self.sub_geographical_regions.remove(sub_geographical_region)
        return self

    @deprecated("Use obj.sub_geographical_regions.clear() instead.")
    def clear_sub_geographical_regions(self) -> GeographicalRegion:
        self.sub_geographical_regions.clear()
        return self

    # endregion sub_geographical_regions boilerplate

    # endregion deprecated list boilerplate
