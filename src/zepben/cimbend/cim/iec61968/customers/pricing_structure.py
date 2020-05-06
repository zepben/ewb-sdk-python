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

__all__ = ["PricingStructure"]


@dataclass
class PricingStructure(Document):
    """
    Grouping of pricing components and prices used in the creation of customer charges and the eligibility
    criteria under which these terms may be offered to a customer. The reasons for grouping include state,
    customer classification, site characteristics, classification (i.e. fee price structure, deposit price
    structure, electric service price structure, etc.) and accounting requirements.

    Attributes -
        _tariffs: Tariffs associated with this PricingStructure
    """
    _tariffs: Optional[Set[Tariff]] = None

    @property
    def num_tariffs(self):
        """
        :return: The number of :class:`zepben.cimbend.iec61968.customers.tariff.Tariff`s associated
        with this ``PricingStructure``
        """
        return nlen(self._tariffs)

    @property
    def tariffs(self) -> Generator[Tariff, None, None]:
        """
        :return: Generator over the ``Tarriff``s of this ``PricingStructure``.
        """
        return ngen(self._tariffs)

    def get_tariff(self, mrid: str) -> Tariff:
        """
        Get the ``Tariff`` for this ``PricingStructure`` identified by ``mrid``

        :param mrid: the mRID of the required :class:`zepben.cimbend.iec61968.customers.tariff.Tariff`
        :return: The :class:`zepben.cimbend.iec61968.customers.tariff.Tariff` with the specified
        ``mrid`` if it exists
        :raises: KeyError if mrid wasn't present.
        """
        return get_by_mrid(self._tariffs, mrid)

    def add_tariff(self, tariff: Tariff) -> PricingStructure:
        """
        :param tariff: the :class:`zepben.cimbend.iec61968.customers.tariff.Tariff` to
        associate with this ``PricingStructure``.
        :return: A reference to this ``PricingStructure`` to allow fluent use.
        """
        require(not contains_mrid(self._tariffs, tariff.mrid), lambda: f"A PricingStructure with mRID {tariff.mrid} "
                                                                       f"already exists in {str(self)}.")
        self._tariffs = set() if self._tariffs is None else self._tariffs
        self._tariffs.add(tariff)
        return self

    def remove_tariff(self, tariff: Tariff) -> PricingStructure:
        """
        :param tariff: the :class:`zepben.cimbend.iec61968.customers.tariff.Tariff` to
        disassociate with this ``PricingStructure``.
        :raises: KeyError if ``tariff`` was not associated with this ``PricingStructure``.
        :return: A reference to this ``PricingStructure`` to allow fluent use.
        """
        if self._tariffs is not None:
            self._tariffs.remove(tariff)
            if not self._tariffs:
                self._tariffs = None
        else:
            raise KeyError(tariff)

        return self

    def clear_tariffs(self) -> PricingStructure:
        """
        Clear all tariffs.
        :return: A reference to this ``PricingStructure`` to allow fluent use.
        """
        self._tariffs = None
        return self
