#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Customer"]

from typing import Optional, Generator, List, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61968.common.organisation_role import OrganisationRole
from zepben.ewb.model.cim.iec61968.customers.customer_kind import CustomerKind
from zepben.ewb.util import nlen, get_by_mrid, ngen, safe_remove

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.customers.customer_agreement import CustomerAgreement


@dataslot
@boilermaker
class Customer(OrganisationRole):
    """
    Organisation receiving services from service supplier.
    """

    kind: CustomerKind = CustomerKind.UNKNOWN
    """Kind of customer"""

    special_need: str | None = None
    """A special service need such as life support, hospitals, etc."""

    customer_agreements: List[CustomerAgreement] | None = MRIDListAccessor()

    def _retype(self):
        self.customer_agreements: MRIDListRouter = ...
    
    @deprecated("BOILERPLATE: Use len(customer_agreements) instead")
    def num_agreements(self) -> int:
        return len(self.customer_agreements)

    @property
    def agreements(self) -> Generator[CustomerAgreement, None, None]:
        """
        The `CustomerAgreement`s for this `Customer`.
        """
        return self.customer_agreements

    @deprecated("BOILERPLATE: Use customer_agreements.get_by_mrid(mrid) instead")
    def get_agreement(self, mrid: str) -> CustomerAgreement:
        return self.customer_agreements.get_by_mrid(mrid)

    @deprecated("BOILERPLATE: Use customer_agreements.append(customer_agreement) instead")
    def add_agreement(self, customer_agreement: CustomerAgreement) -> Customer:
        return self.customer_agreements.append(customer_agreement)

    @deprecated("BOILERPLATE: Use customer_agreements.remove(customer_agreement) instead")
    def remove_agreement(self, customer_agreement: CustomerAgreement) -> Customer:
        return self.customer_agreements.remove(customer_agreement)

    @deprecated("BOILERPLATE: Use customer_agreements.clear() instead")
    def clear_agreements(self) -> Customer:
        return self.customer_agreements.clear()
        return self
