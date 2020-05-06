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

from zepben.cimbend.cim.iec61968.common.document import Document
from zepben.cimbend.util import require, contains_mrid, get_by_mrid, nlen, ngen

__all__ = ["OperationalRestriction"]


@dataclass
class OperationalRestriction(Document):
    """
     A document that can be associated with equipment to describe any sort of restrictions compared with the
     original manufacturer's specification or with the usual operational practice e.g.
     temporary maximum loadings, maximum switching current, do not operate if bus couplers are open, etc.

     In the UK, for example, if a breaker or switch ever mal-operates, this is reported centrally and utilities
     use their asset systems to identify all the installed devices of the same manufacturer's type.
     They then apply operational restrictions in the operational systems to warn operators of potential problems.
     After appropriate inspection and maintenance, the operational restrictions may be removed.
    """
    _equipment: Optional[Set[Equipment]] = None

    def __post_init__(self):
        if self._equipment is not None:
            for equip in self._equipment:
                equip.add_operational_restriction(self)

    @property
    def num_equipment(self):
        """
        :return: The number of :class:`zepben.cimbend.iec61970.base.core.equipment.Equipment`s associated
        with this ``OperationalRestriction``
        """
        return nlen(self._equipment)

    @property
    def equipment(self) -> Generator[Equipment, None, None]:
        """
        :return: Generator over the ``Equipment``s of this ``OperationalRestriction``.
        """
        return ngen(self._equipment)

    def get_equipment(self, mrid: str) -> Equipment:
        """
        Get the ``Equipment`` for this ``OperationalRestriction`` identified by ``mrid``

        :param mrid: the mRID of the required :class:`zepben.cimbend.iec61970.base.core.equipment.Equipment`
        :return: The :class:`zepben.cimbend.iec61970.base.core.equipment.Equipment` with the specified
        ``mrid`` if it exists
        :raises: KeyError if mrid wasn't present.
        """
        return get_by_mrid(self._equipment, mrid)

    def add_equipment(self, equipment: Equipment) -> OperationalRestriction:
        """
        :param equipment: the :class:`zepben.cimbend.iec61970.base.core.equipment.Equipment` to
        associate with this ``OperationalRestriction``.
        :return: A reference to this ``OperationalRestriction`` to allow fluent use.
        """
        require(not contains_mrid(self._equipment, equipment.mrid), lambda: f"An Equipment with mRID {equipment.mrid}"
                                                                            f" already exists in {str(self)}.")
        self._equipment = set() if self._equipment is None else self._equipment
        self._equipment.add(equipment)
        return self

    def remove_equipment(self, equipment: Equipment) -> OperationalRestriction:
        """
        :param equipment: the :class:`zepben.cimbend.iec61970.base.core.equipment.Equipment` to
        disassociate with this ``OperationalRestriction``.
        :raises: KeyError if ``equipment`` was not associated with this ``OperationalRestriction``.
        :return: A reference to this ``OperationalRestriction`` to allow fluent use.
        """
        if self._equipment is not None:
            self._equipment.remove(equipment)
            if not self._equipment:
                self._equipment = None
        else:
            raise KeyError(equipment)

        return self

    def clear_equipment(self) -> OperationalRestriction:
        """
        Clear all equipment.
        :return: A reference to this ``OperationalRestriction`` to allow fluent use.
        """
        self._equipment = None
        return self
