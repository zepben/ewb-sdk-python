#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["CustomerAgreement"]

from typing import Optional, Generator, List, TYPE_CHECKING
from dataclasses import field
from typing_extensions import deprecated

from zepben.ewb.model.cim.iec61968.common.agreement import Agreement
from zepben.ewb.util import nlen, get_by_mrid, ngen, safe_remove
from zepben.ewb.dataclass_descriptors.dataclass_base import zb_dataclass
from zepben.ewb import remove_descriptor_annotations
from zepben.ewb.dataclass_descriptors.mrid_list import MridCollection, LazyMridList

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.customers.customer import Customer
    from zepben.ewb.model.cim.iec61968.customers.pricing_structure import PricingStructure


@zb_dataclass
class CustomerAgreement(Agreement):
    """
    Agreement between the customer and the service supplier to pay for service at a specific service location. It
    records certain billing information about the type of service provided at the service location and is used
    during charge creation to determine the type of service.
    """

    _customer: Optional[Customer] = None
    """The `zepben.ewb.model.cim.iec61968.customers.customer.Customer` that has this `CustomerAgreement`."""

    _pricing_structures: Optional[List[PricingStructure]] = field(default=None)

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


    pricing_structures: MridCollection[PricingStructure] = LazyMridList(
        _pricing_structures,
        "A PricingStructure",
    )


    # region deprecated list boilerplate
    # region pricing_structures boilerplate

    @deprecated("Use len(obj.pricing_structures) instead.")
    def num_pricing_structures(self):
        return len(self.pricing_structures)

    @deprecated("Use obj.pricing_structures.get_by_mrid(mrid) instead.")
    def get_pricing_structure(self, mrid: str) -> PricingStructure:
        return self.pricing_structures.get_by_mrid(mrid)

    @deprecated("Use obj.pricing_structures.append(ps) instead.")
    def add_pricing_structure(self, ps: PricingStructure) -> CustomerAgreement:
        self.pricing_structures.append(ps)
        return self

    @deprecated("Use obj.pricing_structures.remove(ps) instead.")
    def remove_pricing_structure(self, ps: PricingStructure) -> CustomerAgreement:
        self.pricing_structures.remove(ps)
        return self

    @deprecated("Use obj.pricing_structures.clear() instead.")
    def clear_pricing_structures(self) -> CustomerAgreement:
        self.pricing_structures.clear()
        return self

    # endregion pricing_structures boilerplate

    # endregion deprecated list boilerplate
