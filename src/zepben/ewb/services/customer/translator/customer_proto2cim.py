#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["agreement_to_cim", "customer_to_cim", "customer_agreement_to_cim", "pricing_structure_to_cim", "tariff_to_cim"]

from typing import Optional

from zepben.protobuf.cim.iec61968.common.Agreement_pb2 import Agreement as PBAgreement
from zepben.protobuf.cim.iec61968.customers.CustomerAgreement_pb2 import CustomerAgreement as PBCustomerAgreement
from zepben.protobuf.cim.iec61968.customers.Customer_pb2 import Customer as PBCustomer
from zepben.protobuf.cim.iec61968.customers.PricingStructure_pb2 import PricingStructure as PBPricingStructure
from zepben.protobuf.cim.iec61968.customers.Tariff_pb2 import Tariff as PBTariff

import zepben.ewb.services.common.resolver as resolver
from zepben.ewb import organisation_role_to_cim, document_to_cim, BaseService, CustomerKind, bind_to_cim
from zepben.ewb.model.cim.iec61968.common.agreement import Agreement
from zepben.ewb.model.cim.iec61968.customers.customer import Customer
from zepben.ewb.model.cim.iec61968.customers.customer_agreement import CustomerAgreement
from zepben.ewb.model.cim.iec61968.customers.pricing_structure import PricingStructure
from zepben.ewb.model.cim.iec61968.customers.tariff import Tariff
from zepben.ewb.services.common.translator.base_proto2cim import get_nullable
from zepben.ewb.services.customer.customers import CustomerService


###################
# IEC61968 Common #
###################

@bind_to_cim
def agreement_to_cim(pb: PBAgreement, cim: Agreement, service: BaseService):
    document_to_cim(pb.doc, cim, service)


######################
# IEC61968 Customers #
######################

@bind_to_cim
def customer_to_cim(pb: PBCustomer, service: CustomerService) -> Optional[Customer]:
    cim = Customer(
        mrid=pb.mrid(),
        kind=CustomerKind(pb.kind),
        # TODO: missing num_end_devices from jvm sdk
        special_need=get_nullable(pb, 'specialNeed')
    )

    for mrid in pb.customerAgreementMRIDs:
        service.resolve_or_defer_reference(resolver.agreements(cim), mrid)

    organisation_role_to_cim(getattr(pb, 'or'), cim, service)
    return cim if service.add(cim) else None


@bind_to_cim
def customer_agreement_to_cim(pb: PBCustomerAgreement, service: CustomerService) -> Optional[CustomerAgreement]:
    cim = CustomerAgreement(mrid=pb.mrid())

    service.resolve_or_defer_reference(resolver.customer(cim), pb.customerMRID)
    for mrid in pb.pricingStructureMRIDs:
        service.resolve_or_defer_reference(resolver.pricing_structures(cim), mrid)

    agreement_to_cim(pb.agr, cim, service)
    return cim if service.add(cim) else None


@bind_to_cim
def pricing_structure_to_cim(pb: PBPricingStructure, service: CustomerService) -> Optional[PricingStructure]:
    cim = PricingStructure(mrid=pb.mrid())

    for mrid in pb.tariffMRIDs:
        service.resolve_or_defer_reference(resolver.tariffs(cim), mrid)

    document_to_cim(pb.doc, cim, service)
    return cim if service.add(cim) else None


@bind_to_cim
def tariff_to_cim(pb: PBTariff, service: CustomerService) -> Optional[Tariff]:
    # noinspection PyArgumentList
    cim = Tariff(mrid=pb.mrid())

    document_to_cim(pb.doc, cim, service)
    return cim if service.add(cim) else None
