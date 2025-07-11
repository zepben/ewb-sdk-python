#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["SubGeographicalRegion"]

from typing import Optional, List, Generator, TYPE_CHECKING

from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.util import nlen, ngen, get_by_mrid, safe_remove

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.geographical_region import GeographicalRegion
    from zepben.ewb.model.cim.iec61970.base.core.substation import Substation


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
