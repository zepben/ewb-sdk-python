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

from dataclasses import dataclass, InitVar, field
from typing import List, Optional, Generator

from zepben.cimbend.cim.iec61968.assets.structure import Structure
from zepben.cimbend.util import get_by_mrid, ngen, nlen, safe_remove

__all__ = ["Pole"]


@dataclass
class Pole(Structure):
    streetlights_: InitVar[List[Streetlight]] = field(default=list())
    _streetlights: Optional[List[Streetlight]] = field(init=False, default=None)

    def __post_init__(self, organisationroles: List[AssetOrganisationRole], streetlights_: List[Streetlight]):
        super().__post_init__(organisationroles)
        for light in streetlights_:
            self.add_streetlight(light)

    @property
    def num_streetlights(self) -> int:
        """
        Get the number of entries in the :class:`zepben.cimbend.iec61968.assets.streetlight.Streetlight` collection.
        """
        return nlen(self._streetlights)

    @property
    def streetlights(self) -> Generator[Streetlight, None, None]:
        """
        :return: Generator over the ``Streetlight``s of this ``Pole``.
        """
        return ngen(self._streetlights)

    def get_streetlight(self, mrid: str) -> Streetlight:
        """
        Get the ``Streetlight`` for this asset identified by ``mrid``.

        :param mrid: the mRID of the required :class:`zepben.cimbend.iec61968.assets.streetlight.Streetlight`
        :return: The :class:`zepben.cimbend.iec61968.assets.streetlight.Streetlight` with the
        specified ``mrid``.
        :raises: KeyError if mrid wasn't present.
        """
        return get_by_mrid(self._streetlights, mrid)

    def add_streetlight(self, streetlight: Streetlight) -> Pole:
        """
        :param streetlight: the :class:`zepben.cimbend.iec61968.assets.streetlight.Streetlight` to
        associate with this ``Pole``. Will only add to this object if it is not already associated.
        :return: A reference to this ``Pole`` to allow fluent use.
        """
        if self._validate_reference(streetlight, self.get_streetlight, "A Streetlight"):
            return self

        self._streetlights = list() if self._streetlights is None else self._streetlights
        self._streetlights.append(streetlight)
        return self

    def remove_streetlight(self, streetlight: Streetlight) -> Pole:
        """
        :param streetlight: the :class:`zepben.cimbend.iec61968.assets.streetlight.Streetlight` to
        disassociate from this ``Pole``.
        :raises: ValueError if ``streetlight`` was not associated with this ``Pole``.
        :return: A reference to this ``Pole`` to allow fluent use.
        """
        self._streetlights = safe_remove(self._streetlights, streetlight)
        return self

    def clear_streetlights(self) -> Pole:
        """
        Clear all Streetlights.
        :return: self
        """
        self._streetlights = None
        return self
