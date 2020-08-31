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
from typing import Optional, Generator, List

from zepben.cimbend.cim.iec61968.common.document import Agreement
from zepben.cimbend.util import nlen, get_by_mrid, ngen, safe_remove

__all__ = ["CustomerAgreement"]


@dataclass
class CustomerAgreement(Agreement):
    """
    Agreement between the customer and the service supplier to pay for service at a specific service location. It
    records certain billing information about the type of service provided at the service location and is used
    during charge creation to determine the type of service.

    Attributes -
        customer : The ``Customer`` that has this ``CustomerAgreement``.
        pricing_structures : ``PricingStructures`` associated with this CustomerAgreement
    """
    customer: Optional[Customer] = None
    pricingstructures: InitVar[List[PricingStructure]] = field(default=list())
    _pricing_structures: Optional[List[PricingStructure]] = field(init=False, default=None)

    def __post_init__(self, pricingstructures: List[PricingStructure]):
        super().__post_init__()
        for ps in pricingstructures:
            self.add_pricing_structure(ps)

    @property
    def num_pricing_structures(self):
        """
        :return: The number of :class:`zepben.cimbend.iec61968.customers.pricing_structure.PricingStructure`s associated
        with this ``CustomerAgreement``
        """
        return nlen(self._pricing_structures)

    @property
    def pricing_structures(self) -> Generator[PricingStructure, None, None]:
        """
        :return: Generator over the ``PricingStructure``s of this ``CustomerAgreement``.
        """
        return ngen(self._pricing_structures)

    def get_pricing_structure(self, mrid: str) -> PricingStructure:
        """
        Get the ``PricingStructure`` for this ``CustomerAgreement`` identified by ``mrid``

        :param mrid: the mRID of the required :class:`zepben.cimbend.iec61968.customers.pricing_structure.PricingStructure`
        :return: The :class:`zepben.cimbend.iec61968.customers.pricing_structure.PricingStructure` with the specified
        ``mrid`` if it exists
        :raises: KeyError if mrid wasn't present.
        """
        return get_by_mrid(self._pricing_structures, mrid)

    def add_pricing_structure(self, ps: PricingStructure) -> CustomerAgreement:
        """
        :param ps: the :class:`zepben.cimbend.iec61968.customers.pricing_structure.PricingStructure` to
        associate with this ``CustomerAgreement``. Will only add to this object if it is not already associated.
        :return: A reference to this ``CustomerAgreement`` to allow fluent use.
        """
        if self._validate_reference(ps, self.get_pricing_structure, "A PricingStructure"):
            return self

        self._pricing_structures = list() if self._pricing_structures is None else self._pricing_structures
        self._pricing_structures.append(ps)
        return self

    def remove_pricing_structure(self, ps: PricingStructure) -> CustomerAgreement:
        """
        :param ps: the :class:`zepben.cimbend.iec61968.customers.pricing_structure.PricingStructure` to
        disassociate with this ``CustomerAgreement``.
        :raises: ValueError if ``ps`` was not associated with this ``CustomerAgreement``.
        :return: A reference to this ``CustomerAgreement`` to allow fluent use.
        """
        self._pricing_structures = safe_remove(self._pricing_structures, ps)
        return self

    def clear_pricing_structures(self) -> CustomerAgreement:
        """
        Clear all pricing structures.
        :return: A reference to this ``CustomerAgreement`` to allow fluent use.
        """
        self._pricing_structures = None
        return self
