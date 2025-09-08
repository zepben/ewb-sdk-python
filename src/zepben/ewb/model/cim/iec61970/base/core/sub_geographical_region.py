#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["SubGeographicalRegion"]

from typing import Optional, List, TYPE_CHECKING

from zepben.ewb.collections.autoslot import dataslot
from zepben.ewb.collections.mrid_list import MRIDList
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.geographical_region import GeographicalRegion
    from zepben.ewb.model.cim.iec61970.base.core.substation import Substation


@dataslot
class SubGeographicalRegion(IdentifiedObject):
    """
    A subset of a geographical region of a power system network model.
    """

    geographical_region: Optional[GeographicalRegion] = None
    """The geographical region to which this sub-geographical region is within."""

    substations: Optional[List[Substation]] = None

    def __post_init__(self, substations: List[Substation] = None, **kwargs):
        self.substations: MRIDList[Substation] = MRIDList(self.substations)

    def num_substations(self) -> int:
        """
        Returns The number of `Substation`s associated with this `SubGeographicalRegion`
        """
        return len(self.substations)


    def get_substation(self, mrid: str) -> Substation:
        """
        Get the `Substation` for this `SubGeographicalRegion` identified by `mrid`

        `mrid` the mRID of the required `Substation`
        Returns The `Substation` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return self.substations.get_by_mrid(mrid)

    def add_substation(self, substation: Substation) -> SubGeographicalRegion:
        """
        Associate a `Substation` with this `GeographicalRegion`

        `substation` the `Substation` to associate with this `SubGeographicalRegion`.

        Returns A reference to this `SubGeographicalRegion` to allow fluent use.

        Raises `ValueError` if another `Substation` with the same `mrid` already exists for this
        `GeographicalRegion`.
        """
        self.substations.add(substation)
        return self

    def remove_substation(self, substation: Substation) -> SubGeographicalRegion:
        """
        Disassociate `substation` from this `GeographicalRegion`

        `substation` The `Substation` to disassociate from this `SubGeographicalRegion`.
        Returns A reference to this `SubGeographicalRegion` to allow fluent use.
        Raises `ValueError` if `substation` was not associated with this `SubGeographicalRegion`.
        """
        self.substations.remove(substation)
        return self

    def clear_substations(self) -> SubGeographicalRegion:
        """
        Clear all `Substations`.
        Returns A reference to this `SubGeographicalRegion` to allow fluent use.
        """
        self.substations.clear()
        return self
