#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional, Generator, List, TYPE_CHECKING

if TYPE_CHECKING:
    from zepben.evolve import PricingStructure, Customer

from zepben.evolve.model.cim.iec61968.common.document import Agreement
from zepben.evolve.util import nlen, get_by_mrid, ngen, safe_remove

__all__ = ["CustomerAgreement"]


class CustomerAgreement(Agreement):
    """
    Agreement between the customer and the service supplier to pay for service at a specific service location. It
    records certain billing information about the type of service provided at the service location and is used
    during charge creation to determine the type of service.
    """

    _customer: Optional[Customer] = None
    """The `zepben.evolve.cim.iec61968.customers.customer.Customer` that has this `CustomerAgreement`."""

    _pricing_structures: Optional[List[PricingStructure]] = None

    def __init__(self, customer: Customer = None, pricing_structures: List[PricingStructure] = None, **kwargs):
        super(CustomerAgreement, self).__init__(**kwargs)
        if customer:
            self.customer = customer
        if pricing_structures:
            for ps in pricing_structures:
                self.add_pricing_structure(ps)

    @property
    def customer(self):
        """The `Customer` that has this `CustomerAgreement`."""
        return self._customer

    @customer.setter
    def customer(self, cust):
        if self._customer is None or self._customer is cust:
            self._customer = cust
        else:
            raise ValueError(f"customer for {str(self)} has already been set to {self._customer}, cannot reset this field to {cust}")

    def num_pricing_structures(self):
        """
        The number of `PricingStructure`s associated with this `CustomerAgreement`
        """
        return nlen(self._pricing_structures)

    @property
    def pricing_structures(self) -> Generator[PricingStructure, None, None]:
        """
        The `PricingStructure`s of this `CustomerAgreement`.
        """
        return ngen(self._pricing_structures)

    def get_pricing_structure(self, mrid: str) -> PricingStructure:
        """
        Get the `PricingStructure` for this `CustomerAgreement` identified by `mrid`

        `mrid` the mRID of the required `PricingStructure`
        Returns the `PricingStructure` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._pricing_structures, mrid)

    def add_pricing_structure(self, ps: PricingStructure) -> CustomerAgreement:
        """
        Associate `ps` with this `CustomerAgreement`

        `ps` the `PricingStructure` to associate with this `CustomerAgreement`.
        Returns A reference to this `CustomerAgreement` to allow fluent use.
        Raises `ValueError` if another `PricingStructure` with the same `mrid` already exists for this `CustomerAgreement`
        """
        if self._validate_reference(ps, self.get_pricing_structure, "A PricingStructure"):
            return self

        self._pricing_structures = list() if self._pricing_structures is None else self._pricing_structures
        self._pricing_structures.append(ps)
        return self

    def remove_pricing_structure(self, ps: PricingStructure) -> CustomerAgreement:
        """
        Disassociate `ps` from this `CustomerAgreement`

        `ps` the `PricingStructure` to disassociate from this `CustomerAgreement`.
        Returns A reference to this `CustomerAgreement` to allow fluent use.
        Raises `ValueError` if `ps` was not associated with this `CustomerAgreement`.
        """
        self._pricing_structures = safe_remove(self._pricing_structures, ps)
        return self

    def clear_pricing_structures(self) -> CustomerAgreement:
        """
        Clear all pricing structures.
        Returns a reference to this `CustomerAgreement` to allow fluent use.
        """
        self._pricing_structures = None
        return self
