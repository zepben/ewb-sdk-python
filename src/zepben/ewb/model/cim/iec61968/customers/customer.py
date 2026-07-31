#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Customer"]

from typing import Optional, List, TYPE_CHECKING
from dataclasses import field
from typing_extensions import deprecated

from zepben.ewb.model.cim.iec61968.common.organisation_role import OrganisationRole
from zepben.ewb.model.cim.iec61968.customers.customer_kind import CustomerKind
from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb import Alias
from zepben.ewb.boilerplate.collections.mrid_list import LazyMridList
from zepben.ewb.boilerplate.collections.mrid_collection import MridCollection

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.customers.customer_agreement import CustomerAgreement


@zb_dataclass
class Customer(OrganisationRole):
    """
    Organisation receiving services from service supplier.
    """

    kind: CustomerKind = CustomerKind.UNKNOWN
    """Kind of customer"""

    special_need: Optional[str] = None
    """A special service need such as life support, hospitals, etc."""

    _customer_agreements: Optional[List[CustomerAgreement]] = field(default=None)

    def __init__(self, *args, customer_agreements=None, **kwargs):
        super(Customer, self).__init__(*args, **kwargs)
        self.agreements.extend(customer_agreements)

    agreements: MridCollection[CustomerAgreement] = LazyMridList(
        _customer_agreements,
        "A CustomerAgreement",
    )

    # region deprecated list boilerplate
    # region agreements boilerplate

    @deprecated("Use len(obj.agreements) instead.")
    def num_agreements(self) -> int:
        return len(self.agreements)

    @deprecated("Use obj.agreements.get_by_mrid(mrid) instead.")
    def get_agreement(self, mrid: str) -> CustomerAgreement:
        return self.agreements.get_by_mrid(mrid)

    @deprecated("Use obj.agreements.append(customer_agreement) instead.")
    def add_agreement(self, customer_agreement: CustomerAgreement) -> Customer:
        self.agreements.append(customer_agreement)
        return self

    @deprecated("Use obj.agreements.remove(customer_agreement) instead.")
    def remove_agreement(self, customer_agreement: CustomerAgreement) -> Customer:
        self.agreements.remove(customer_agreement)
        return self

    @deprecated("Use obj.agreements.clear() instead.")
    def clear_agreements(self) -> Customer:
        self.agreements.clear()
        return self

    # endregion agreements boilerplate

    # endregion deprecated list boilerplate
