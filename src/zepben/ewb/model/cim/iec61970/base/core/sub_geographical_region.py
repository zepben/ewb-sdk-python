#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["SubGeographicalRegion"]

from typing import List, TYPE_CHECKING

from typing_extensions import deprecated

from zepben.ewb.dataslot import MRIDListRouter, dataslot, MRIDListAccessor
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.geographical_region import GeographicalRegion
    from zepben.ewb.model.cim.iec61970.base.core.substation import Substation


@dataslot
class SubGeographicalRegion(IdentifiedObject):
    """
    A subset of a geographical region of a power system network model.
    """

    geographical_region: GeographicalRegion | None = None
    """The geographical region to which this sub-geographical region is within."""

    substations: List[Substation] | None = MRIDListAccessor()

    def _retype(self):
        self.substations: MRIDListRouter[Substation] = ...
    
    @deprecated("BOILERPLATE: Use len(substations) instead")
    def num_substations(self) -> int:
        return len(self.substations)

    @deprecated("BOILERPLATE: Use substations.get_by_mrid(mrid) instead")
    def get_substation(self, mrid: str) -> Substation:
        return self.substations.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use substations.append(substation) instead")
    def add_substation(self, substation: Substation) -> SubGeographicalRegion:
        self.substations.append(substation)
        return self

    @deprecated("Boilerplate: Use substations.remove(substation) instead")
    def remove_substation(self, substation: Substation) -> SubGeographicalRegion:
        self.substations.remove(substation)
        return self

    @deprecated("BOILERPLATE: Use substations.clear() instead")
    def clear_substations(self) -> SubGeographicalRegion:
        self.substations.clear()
        return self

