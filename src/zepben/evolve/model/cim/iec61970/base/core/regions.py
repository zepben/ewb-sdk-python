#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional, Generator, List, TYPE_CHECKING

if TYPE_CHECKING:
    from zepben.evolve import Substation

from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.evolve.util import nlen, get_by_mrid, ngen, safe_remove

__all__ = ["GeographicalRegion", "SubGeographicalRegion"]


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


class SubGeographicalRegion(IdentifiedObject):
    """
    A subset of a geographical region of a power system network model.
    """

    geographical_region: Optional[GeographicalRegion] = None
    """The geographical region to which this sub-geographical region is within."""

    _substations: Optional[List[Substation]] = None

    def __init__(self, substations: List[Substation] = None, **kwargs):
        super(SubGeographicalRegion, self).__init__(**kwargs)
        if substations:
            for sub in substations:
                self.add_substation(sub)

    def num_substations(self) -> int:
        """
        Returns The number of `Substation`s associated with this `SubGeographicalRegion`
        """
        return nlen(self._substations)

    @property
    def substations(self) -> Generator[Substation, None, None]:
        """
        All substations belonging to this sub geographical region.
        """
        return ngen(self._substations)

    def get_substation(self, mrid: str) -> Substation:
        """
        Get the `Substation` for this `SubGeographicalRegion` identified by `mrid`

        `mrid` the mRID of the required `Substation`
        Returns The `Substation` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._substations, mrid)

    def add_substation(self, substation: Substation) -> SubGeographicalRegion:
        """
        Associate a `Substation` with this `GeographicalRegion`

        `substation` the `Substation` to associate with this `SubGeographicalRegion`.

        Returns A reference to this `SubGeographicalRegion` to allow fluent use.

        Raises `ValueError` if another `Substation` with the same `mrid` already exists for this
        `GeographicalRegion`.
        """
        if self._validate_reference(substation, self.get_substation, "A Substation"):
            return self
        self._substations = list() if self._substations is None else self._substations
        self._substations.append(substation)
        return self

    def remove_substation(self, substation: Substation) -> SubGeographicalRegion:
        """
        Disassociate `substation` from this `GeographicalRegion`

        `substation` The `Substation` to disassociate from this `SubGeographicalRegion`.
        Returns A reference to this `SubGeographicalRegion` to allow fluent use.
        Raises `ValueError` if `substation` was not associated with this `SubGeographicalRegion`.
        """
        self._substations = safe_remove(self._substations, substation)
        return self

    def clear_substations(self) -> SubGeographicalRegion:
        """
        Clear all `Substations`.
        Returns A reference to this `SubGeographicalRegion` to allow fluent use.
        """
        self._substations = None
        return self
