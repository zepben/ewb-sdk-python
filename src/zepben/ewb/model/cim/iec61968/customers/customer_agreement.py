#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["CustomerAgreement"]

from typing import Optional, Generator, List, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61968.common.agreement import Agreement
from zepben.ewb.util import nlen, get_by_mrid, ngen, safe_remove

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.customers.customer import Customer
    from zepben.ewb.model.cim.iec61968.customers.pricing_structure import PricingStructure


@dataslot
class CustomerAgreement(Agreement):
    """
    Agreement between the customer and the service supplier to pay for service at a specific service location. It
    records certain billing information about the type of service provided at the service location and is used
    during charge creation to determine the type of service.
    """

    customer: Customer | None = NoResetDescriptor(None)
    """The `zepben.ewb.model.cim.iec61968.customers.customer.Customer` that has this `CustomerAgreement`."""

    pricing_structures: List[PricingStructure] | None = MRIDListAccessor()

    def _retype(self):
        self.pricing_structures: MRIDListRouter[PricingStructure] = ...

    @deprecated("BOILERPLATE: Use len(pricing_structures) instead")
    def num_pricing_structures(self):
        return len(self.pricing_structures)

    @deprecated("BOILERPLATE: Use pricing_structures.get_by_mrid(mrid) instead")
    def get_pricing_structure(self, mrid: str) -> PricingStructure:
        return self.pricing_structures.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use pricing_structures.append(ps) instead")
    def add_pricing_structure(self, ps: PricingStructure) -> CustomerAgreement:
        self.pricing_structures.append(ps)
        return self

    @deprecated("Boilerplate: Use pricing_structures.remove(ps) instead")
    def remove_pricing_structure(self, ps: PricingStructure) -> CustomerAgreement:
        self.pricing_structures.remove(ps)
        return self

    @deprecated("BOILERPLATE: Use pricing_structures.clear() instead")
    def clear_pricing_structures(self) -> CustomerAgreement:
        self.pricing_structures.clear()
        return self

