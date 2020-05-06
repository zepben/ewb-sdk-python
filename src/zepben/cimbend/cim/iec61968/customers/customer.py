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

from zepben.cimbend.cim.iec61968.common.organisation_role import OrganisationRole
from zepben.cimbend.cim.iec61968.customers.customer_kind import CustomerKind
from zepben.cimbend.util import nlen, get_by_mrid, require, contains_mrid, ngen

__all__ = ["Customer"]


@dataclass
class Customer(OrganisationRole):
    """
    Organisation receiving services from service supplier.

    Attributes -
        kind : Kind of customer
        numEndDevices : The number of end devices associated with this customer
    """
    kind: CustomerKind = CustomerKind.UNKNOWN
    _customer_agreements: Optional[Set[CustomerAgreement]] = None
    num_end_devices: int = 0

    @property
    def num_agreements(self) -> int:
        """
        Get the number of :class:`customer_agreement.CustomerAgreement`s associated with this ``Customer``.
        """
        return nlen(self._customer_agreements)

    @property
    def agreements(self) -> Generator[CustomerAgreement, None, None]:
        """
        :return: Generator over the ``CustomerAgreement``s of this ``Customer``.
        """
        return ngen(self._customer_agreements)

    def get_agreement(self, mrid: str) -> CustomerAgreement:
        """
        Get the ``CustomerAgreement`` for this ``Customer`` identified by ``mrid``.

        :param mrid: the mRID of the required :class:`customer_agreement.CustomerAgreement`
        :return: The :class:`customer_agreement.CustomerAgreement` with the specified ``mrid``.
        :raises: KeyError if mrid wasn't present.
        """
        return get_by_mrid(self._customer_agreements, mrid)

    def add_agreement(self, customer_agreement: CustomerAgreement) -> Customer:
        """
        Add a ``CustomerAgreement`` to this ``Customer``.
        :param customer_agreement: the :class:`customer_agreement.CustomerAgreement` to associate with this ``Customer``.
        :return: A reference to this ``Customer`` to allow fluent use.
        """
        require(not contains_mrid(self._customer_agreements, customer_agreement.mrid),
                lambda: f"A CustomerAgreement with mRID {customer_agreement.mrid} already exists in {str(self)}.")
        self._customer_agreements = set() if self._customer_agreements is None else self._customer_agreements
        self._customer_agreements.add(customer_agreement)
        return self

    def remove_agreement(self, customer_agreement: CustomerAgreement) -> Customer:
        """
        Disassociate a ``CustomerAgreement`` from this ``Customer``.
        :param customer_agreement: the :class:`customer_agreement.CustomerAgreement` to
        disassociate with this ``Customer``.
        :raises: KeyError if ``customer_agreement`` was not associated with this ``Customer``.
        """
        if self._customer_agreements is not None:
            self._customer_agreements.remove(customer_agreement)
            if not self._customer_agreements:
                self._customer_agreements = None
        else:
            raise KeyError(customer_agreement)

        return self

    def clear_agreements(self) -> Customer:
        """
        Clear all customer agreements.
        :return: self
        """
        self._customer_agreements = None
        return self
