"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Set, Generator

from zepben.cimbend.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.cimbend.util import nlen, get_by_mrid, contains_mrid, require, ngen

__all__ = ["GeographicalRegion", "SubGeographicalRegion"]


@dataclass
class GeographicalRegion(IdentifiedObject):
    """
    A geographical region of a power system network phases.
    """
    _sub_geographical_regions: Optional[Set[SubGeographicalRegion]] = None

    @property
    def num_sub_geographical_regions(self) -> int:
        """
        :return: The number of :class:`SubGeographicalRegion`s associated with this ``GeographicalRegion``
        """
        return nlen(self._sub_geographical_regions)

    @property
    def sub_geographical_regions(self) -> Generator[SubGeographicalRegion, None, None]:
        """
        :return: Generator over the ``SubGeographicalRegion``s of this ``EquipmentContainer``.
        """
        return ngen(self._sub_geographical_regions)

    def get_sub_geographical_region(self, mrid: str) -> SubGeographicalRegion:
        """
        Get the ``SubGeographicalRegion`` for this ``GeographicalRegion`` identified by ``mrid``

        :param mrid: the mRID of the required :class:`SubGeographicalRegion`
        :return: The :class:`SubGeographicalRegion` with the specified ``mrid`` if it exists
        :raises: KeyError if mrid wasn't present.
        """
        return get_by_mrid(self._sub_geographical_regions, mrid)

    def add_sub_geographical_region(self, sub_geographical_region: SubGeographicalRegion) -> GeographicalRegion:
        """
        :param sub_geographical_region: the :class:`SubGeographicalRegion` to associate with this ``GeographicalRegion``.
        :return: A reference to this ``GeographicalRegion`` to allow fluent use.
        """
        require(not contains_mrid(self._sub_geographical_regions, sub_geographical_region.mrid),
                lambda: f"A SubGeographicalRegion with mRID {sub_geographical_region.mrid} already exists in {str(self)}.")
        self._sub_geographical_regions = set() if self._sub_geographical_regions is None else self._sub_geographical_regions
        self._sub_geographical_regions.add(sub_geographical_region)
        return self

    def remove_sub_geographical_region(self, sub_geographical_region: SubGeographicalRegion) -> GeographicalRegion:
        """
        :param sub_geographical_region: The :class:`SubGeographicalRegion` to disassociate from this ``GeographicalRegion``.
        :raises: KeyError if ``sub_geographical_region`` was not associated with this ``GeographicalRegion``.
        :return: A reference to this ``GeographicalRegion`` to allow fluent use.
        """
        if self._sub_geographical_regions is not None:
            self._sub_geographical_regions.remove(sub_geographical_region)
            if not self._sub_geographical_regions:
                self._sub_geographical_regions = None
        else:
            raise KeyError(sub_geographical_region)

        return self

    def clear_sub_geographical_regions(self) -> GeographicalRegion:
        """
        Clear all SubGeographicalRegions.
        :return: A reference to this ``GeographicalRegion`` to allow fluent use.
        """
        self._sub_geographical_regions = None
        return self


@dataclass
class SubGeographicalRegion(IdentifiedObject):
    geographical_region: Optional[GeographicalRegion] = None
    _substations: Optional[Set[Substation]] = None

    @property
    def num_substations(self) -> int:
        """
        :return: The number of :class:`substation.Substation`s associated with this ``SubGeographicalRegion``
        """
        return nlen(self._substations)

    @property
    def substations(self) -> Generator[Substation, None, None]:
        """
        :return: Generator over the ``Substation``s of this ``EquipmentContainer``.
        """
        return ngen(self._substations)

    def get_substation(self, mrid: str) -> Substation:
        """
        Get the ``Substation`` for this ``SubGeographicalRegion`` identified by ``mrid``

        :param mrid: the mRID of the required :class:`Substation`
        :return: The :class:`Substation` with the specified ``mrid`` if it exists
        :raises: KeyError if mrid wasn't present.
        """
        return get_by_mrid(self._substations, mrid)

    def add_substation(self, substation: Substation) -> SubGeographicalRegion:
        """
        :param substation: the :class:`substation.Substation` to associate with this ``SubGeographicalRegion``.
        :return: A reference to this ``SubGeographicalRegion`` to allow fluent use.
        """
        require(not contains_mrid(self._substations, substation.mrid),
                lambda: f"A Substation with mRID {substation.mrid} already exists in {str(self)}.")
        self._substations = set() if self._substations is None else self._substations
        self._substations.add(substation)
        return self

    def remove_substation(self, substation: Substation) -> SubGeographicalRegion:
        """
        :param substation: The :class:`substation.Substation` to disassociate from this ``SubGeographicalRegion``.
        :raises: KeyError if ``substation`` was not associated with this ``SubGeographicalRegion``.
        :return: A reference to this ``SubGeographicalRegion`` to allow fluent use.
        """
        if self._substations is not None:
            self._substations.remove(substation)
            if not self._substations:
                self._substations = None
        else:
            raise KeyError(substation)

        return self

    def clear_substations(self) -> SubGeographicalRegion:
        """
        Clear all ``Substations``.
        :return: A reference to this ``SubGeographicalRegion`` to allow fluent use.
        """
        self._substations = None
        return self
