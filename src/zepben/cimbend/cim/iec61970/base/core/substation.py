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

from dataclasses import dataclass, field, InitVar
from typing import Optional, Generator, List

from zepben.cimbend.cim.iec61970.base.core.equipment_container import EquipmentContainer
from zepben.cimbend.cim.iec61970.base.core.regions import SubGeographicalRegion
from zepben.cimbend.util import nlen, get_by_mrid, contains_mrid, require, ngen

__all__ = ["Substation"]


@dataclass
class Substation(EquipmentContainer):
    sub_geographical_region: Optional[SubGeographicalRegion] = None
    normalenergizedfeeders: InitVar[List[Feeder]] = field(default=list())
    _normal_energized_feeders: Optional[List[Feeder]] = field(init=False, default=None)

    def __post_init__(self, equipment_: List[Equipment], normalenergizedfeeders: List[Feeder]):
        super().__post_init__(equipment_)
        for feeder in normalenergizedfeeders:
            self.add_feeder(feeder)

    @property
    def num_feeders(self):
        """
        :return: The number of :class:`zepben.cimbend.iec61970.base.core.equipment_container.Feeder`s associated
        with this ``Substation``
        """
        return nlen(self._normal_energized_feeders)

    @property
    def feeders(self) -> Generator[Feeder, None, None]:
        """
        :return: Generator over the normal ``Feeder``s of this ``Equipment``.
        """
        return ngen(self._normal_energized_feeders)

    def get_feeder(self, mrid: str) -> Substation:
        """
        Get the ``Feeder`` for this ``Substation`` identified by ``mrid``

        :param mrid: the mRID of the required :class:`zepben.cimbend.iec61970.base.core.equipment_container.Feeder`
        :return: The :class:`zepben.cimbend.iec61970.base.core.equipment_container.Feeder` with the specified
        ``mrid`` if it exists
        :raises: KeyError if mrid wasn't present.
        """
        return get_by_mrid(self._normal_energized_feeders, mrid)

    def add_feeder(self, feeder: Feeder) -> Substation:
        """
        :param feeder: the :class:`zepben.cimbend.iec61970.base.core.equipment_container.Feeder` to
        associate with this ``Substation``.
        :return: A reference to this ``Substation`` to allow fluent use.
        """
        require(not contains_mrid(self._normal_energized_feeders, feeder.mrid),
                lambda: f"A Feeder with mRID {feeder.mrid} already exists in {str(self)}.")
        self._normal_energized_feeders = list() if self._normal_energized_feeders is None else self._normal_energized_feeders
        self._normal_energized_feeders.append(feeder)
        return self

    def remove_feeder(self, feeder: Feeder) -> Substation:
        """
        :param feeder: the :class:`zepben.cimbend.iec61970.base.core.equipment_container.Feeder` to
        disassociate with this ``Substation``.
        :raises: KeyError if ``feeder`` was not associated with this ``Substation``.
        :return: A reference to this ``Substation`` to allow fluent use.
        """
        if self._normal_energized_feeders is not None:
            self._normal_energized_feeders.remove(feeder)
            if not self._normal_energized_feeders:
                self._normal_energized_feeders = None
        else:
            raise KeyError(feeder)

        return self

    def clear_feeders(self) -> Substation:
        """
        Clear all current ``Feeder``s.
        :return: A reference to this ``Substation`` to allow fluent use.
        """
        self._normal_energized_feeders = None
        return self
