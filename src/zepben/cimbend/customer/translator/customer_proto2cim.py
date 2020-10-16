#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations
import zepben.cimbend.common.resolver as resolver

from zepben.cimbend.common import BaseService
from zepben.protobuf.cim.iec61968.common.Agreement_pb2 import Agreement as PBAgreement
from zepben.protobuf.cim.iec61968.customers.CustomerAgreement_pb2 import CustomerAgreement as PBCustomerAgreement
from zepben.protobuf.cim.iec61968.customers.CustomerKind_pb2 import CustomerKind as PBCustomerKind
from zepben.protobuf.cim.iec61968.customers.Customer_pb2 import Customer as PBCustomer
from zepben.protobuf.cim.iec61968.customers.PricingStructure_pb2 import PricingStructure as PBPricingStructure
from zepben.protobuf.cim.iec61968.customers.Tariff_pb2 import Tariff as PBTariff

from zepben.cimbend.cim.iec61968.customers.customer import Customer
from zepben.cimbend.customer.customers import CustomerService
from zepben.cimbend.common.translator.base_proto2cim import *
from zepben.cimbend.cim.iec61968.common.document import Agreement
from zepben.cimbend.cim.iec61968.customers import CustomerAgreement, CustomerKind, PricingStructure, Tariff

__all__ = ["agreement_to_cim", "tariff_to_cim", "customer_to_cim", "customeragreement_to_cim", "pricingstructure_to_cim"]


def agreement_to_cim(pb: PBAgreement, cim: Agreement, service: BaseService):
    document_to_cim(pb.doc, cim, service)


def customer_to_cim(pb: PBCustomer, service: CustomerService):
    cim = Customer(mrid=pb.mrid(), kind=CustomerKind[PBCustomerKind.Name(pb.kind)])
    for mrid in pb.customerAgreementMRIDs:
        service.resolve_or_defer_reference(resolver.agreements(cim), mrid)
    organisationrole_to_cim(getattr(pb, 'or'), cim)
    service.add(cim)


def customeragreement_to_cim(pb: PBCustomerAgreement, service: CustomerService):
    cim = CustomerAgreement(mrid=pb.mrid())
    service.resolve_or_defer_reference(resolver.customer(cim), pb.customerMRID)
    for mrid in pb.pricingStructureMRIDs:
        service.resolve_or_defer_reference(resolver.pricing_structures(cim), mrid)
    agreement_to_cim(pb.agr, cim, service)
    service.add(cim)


def pricingstructure_to_cim(pb: PBPricingStructure, service: CustomerService):
    cim = PricingStructure(mrid=pb.mrid())
    for mrid in pb.tariffMRIDs:
        service.resolve_or_defer_reference(resolver.tariffs(cim), mrid)
    document_to_cim(pb.doc, cim, service)
    service.add(cim)


def tariff_to_cim(self, pb: PBTariff, service: CustomerService):
    cim = Tariff(mrid=pb.mrid())
    document_to_cim(pb.doc, cim, self.service)
    service.add(cim)


PBAgreement.to_cim = agreement_to_cim
PBCustomer.to_cim = customer_to_cim
PBCustomerAgreement.to_cim = customeragreement_to_cim
PBPricingStructure.to_cim = pricingstructure_to_cim
PBTariff.to_cim = PBTariff
