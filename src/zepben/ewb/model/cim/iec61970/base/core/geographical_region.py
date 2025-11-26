#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["GeographicalRegion"]

from typing import List

from typing_extensions import deprecated

from zepben.ewb.dataslot import MRIDListRouter, dataslot, MRIDListAccessor
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.model.cim.iec61970.base.core.sub_geographical_region import SubGeographicalRegion


@dataslot
class GeographicalRegion(IdentifiedObject):
    """
    A geographical region of a power system network phases.
    """
    sub_geographical_regions: List[SubGeographicalRegion] | None = MRIDListAccessor()

    def _retype(self):
        self.sub_geographical_regions: MRIDListRouter[SubGeographicalRegion] = ...
    
    @deprecated("BOILERPLATE: Use len(sub_geographical_regions) instead")
    def num_sub_geographical_regions(self) -> int:
        return len(self.sub_geographical_regions)

    @deprecated("BOILERPLATE: Use sub_geographical_regions.get_by_mrid(mrid) instead")
    def get_sub_geographical_region(self, mrid: str) -> SubGeographicalRegion:
        return self.sub_geographical_regions.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use sub_geographical_regions.append(sub_geographical_region) instead")
    def add_sub_geographical_region(self, sub_geographical_region: SubGeographicalRegion) -> GeographicalRegion:
        self.sub_geographical_regions.append(sub_geographical_region)
        return self

    @deprecated("Boilerplate: Use sub_geographical_regions.remove(sub_geographical_region) instead")
    def remove_sub_geographical_region(self, sub_geographical_region: SubGeographicalRegion) -> GeographicalRegion:
        self.sub_geographical_regions.remove(sub_geographical_region)
        return self

    @deprecated("BOILERPLATE: Use sub_geographical_regions.clear() instead")
    def clear_sub_geographical_regions(self) -> GeographicalRegion:
        self.sub_geographical_regions.clear()
        return self

