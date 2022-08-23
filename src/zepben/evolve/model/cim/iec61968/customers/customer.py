#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional, Generator, List, TYPE_CHECKING

if TYPE_CHECKING:
    from zepben.evolve import CustomerAgreement

from zepben.evolve.model.cim.iec61968.common.organisation_role import OrganisationRole
from zepben.evolve.model.cim.iec61968.customers.customer_kind import CustomerKind
from zepben.evolve.util import nlen, get_by_mrid, ngen, safe_remove

__all__ = ["Customer"]


class Customer(OrganisationRole):
    """
    Organisation receiving services from service supplier.
    """

    kind: CustomerKind = CustomerKind.UNKNOWN
    """Kind of customer"""

    _customer_agreements: Optional[List[CustomerAgreement]] = None

    def __init__(self, customer_agreements: List[CustomerAgreement] = None, **kwargs):
        super(Customer, self).__init__(**kwargs)
        if customer_agreements:
            for agreement in customer_agreements:
                self.add_agreement(agreement)

    def num_agreements(self) -> int:
        """
        Get the number of `CustomerAgreement`s associated with this `Customer`.
        """
        return nlen(self._customer_agreements)

    @property
    def agreements(self) -> Generator[CustomerAgreement, None, None]:
        """
        The `CustomerAgreement`s for this `Customer`.
        """
        return ngen(self._customer_agreements)

    def get_agreement(self, mrid: str) -> CustomerAgreement:
        """
        Get the `CustomerAgreement` for this `Customer` identified by `mrid`.

        `mrid` the mRID of the required `customer_agreement.CustomerAgreement`
        Returns the `CustomerAgreement` with the specified `mrid`.
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._customer_agreements, mrid)

    def add_agreement(self, customer_agreement: CustomerAgreement) -> Customer:
        """
        Associate a `CustomerAgreement` with this `Customer`.
        `customer_agreement` The `customer_agreement.CustomerAgreement` to associate with this `Customer`.
        Returns A reference to this `Customer` to allow fluent use.
        Raises `ValueError` if another `CustomerAgreement` with the same `mrid` already exists for this `Customer`
        """
        if self._validate_reference(customer_agreement, self.get_agreement, "A CustomerAgreement"):
            return self

        self._customer_agreements = list() if self._customer_agreements is None else self._customer_agreements
        self._customer_agreements.append(customer_agreement)
        return self

    def remove_agreement(self, customer_agreement: CustomerAgreement) -> Customer:
        """
        Disassociate `customer_agreement` from this `Customer`.

        `customer_agreement` the `customer_agreement.CustomerAgreement` to disassociate with this `Customer`.
        Returns A reference to this `Customer` to allow fluent use.
        Raises `ValueError` if `customer_agreement` was not associated with this `Customer`.
        """
        self._customer_agreements = safe_remove(self._customer_agreements, customer_agreement)
        return self

    def clear_agreements(self) -> Customer:
        """
        Clear all customer agreements.
        Returns self
        """
        self._customer_agreements = None
        return self
