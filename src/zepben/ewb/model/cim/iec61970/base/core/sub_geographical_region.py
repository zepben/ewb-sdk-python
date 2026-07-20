#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["SubGeographicalRegion"]

from typing import Optional, List, Generator, TYPE_CHECKING
from dataclasses import field
from typing_extensions import deprecated

from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.util import nlen, ngen, get_by_mrid, safe_remove, require
from zepben.ewb.dataclass_descriptors.dataclass_base import zb_dataclass
from zepben.ewb import remove_descriptor_annotations
from zepben.ewb.dataclass_descriptors.mrid_list import MridCollection, LazyMridList, Backfill
from zepben.ewb.model.cim.iec61970.base.core.substation import Substation

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.geographical_region import GeographicalRegion


@zb_dataclass
class SubGeographicalRegion(IdentifiedObject):
    """
    A subset of a geographical region of a power system network model.
    """

    geographical_region: Optional[GeographicalRegion] = field(default=None)
    """The geographical region to which this sub-geographical region is within."""

    _substations: Optional[List[Substation]] = field(default=None)

    def __init__(self, *args, substations: List[Substation] = None, **kwargs):
        super(SubGeographicalRegion, self).__init__(*args, **kwargs)
        if substations:
            for sub in substations:
                self.add_substation(sub)


    @property
    def geographical_region(self):
        """The geographical region to which this sub-geographical region is within."""
        return self._geographical_region

    @geographical_region.setter
    @deprecated("geographical_region should never be set directly - it is automatically set when adding it to the `sub_geographical_regions` list")
    def geographical_region(self, value):
        self._geographical_region = value

    def num_substations(self) -> int:
        """
        Returns The number of `Substation`s associated with this `SubGeographicalRegion`
        """
        return nlen(self._substations)

    substations: MridCollection[Substation] = LazyMridList(
        _substations,
        "A Substation",
        backfill=Backfill(Substation.sub_geographical_region)
    )


    # region deprecated list boilerplate
    # region substations boilerplate

    @deprecated("Use len(obj.substations) instead.")
    def num_substations(self) -> int:
        return len(self.substations)

    @deprecated("Use obj.substations.get_by_mrid(mrid) instead.")
    def get_substation(self, mrid: str) -> Substation:
        return self.substations.get_by_mrid(mrid)

    @deprecated("Use obj.substations.append(substation) instead.")
    def add_substation(self, substation: Substation) -> SubGeographicalRegion:
        self.substations.append(substation)
        return self

    @deprecated("Use obj.substations.remove(substation) instead.")
    def remove_substation(self, substation: Substation) -> SubGeographicalRegion:
        self.substations.remove(substation)
        return self

    @deprecated("Use obj.substations.clear() instead.")
    def clear_substations(self) -> SubGeographicalRegion:
        self.substations.clear()
        return self

    # endregion substations boilerplate

    # endregion deprecated list boilerplate
