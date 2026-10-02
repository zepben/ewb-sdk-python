#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["CustomerService"]

from typing import Optional

from zepben.ewb.model.cim.iec61968.common.organisation import Organisation
from zepben.ewb.model.cim.iec61968.customers.customer import Customer
from zepben.ewb.model.cim.iec61968.customers.customer_agreement import CustomerAgreement
from zepben.ewb.model.cim.iec61968.customers.pricing_structure import PricingStructure
from zepben.ewb.model.cim.iec61968.customers.tariff import Tariff
from zepben.ewb.services.common.base_service import BaseService
from zepben.ewb.services.common.meta.metadata_collection import MetadataCollection


class CustomerService(BaseService):
    """
    Used to store Customer related types.
    """

    supported_types = {Customer, CustomerAgreement, Organisation, PricingStructure, Tariff}

    def __init__(
        self,
        metadata: Optional[MetadataCollection] = None
    ):
        super().__init__("customer", metadata)
