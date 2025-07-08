#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["agreement_to_pb", "customer_to_pb", "customer_agreement_to_pb", "pricing_structure_to_pb", "tariff_to_pb"]

from zepben.protobuf.cim.iec61968.common.Agreement_pb2 import Agreement as PBAgreement
from zepben.protobuf.cim.iec61968.customers.CustomerAgreement_pb2 import CustomerAgreement as PBCustomerAgreement
from zepben.protobuf.cim.iec61968.customers.Customer_pb2 import Customer as PBCustomer
from zepben.protobuf.cim.iec61968.customers.PricingStructure_pb2 import PricingStructure as PBPricingStructure
from zepben.protobuf.cim.iec61968.customers.Tariff_pb2 import Tariff as PBTariff

from zepben.ewb.model.cim.iec61968.common.agreement import Agreement
from zepben.ewb.model.cim.iec61968.customers.customer import Customer
from zepben.ewb.model.cim.iec61968.customers.customer_agreement import CustomerAgreement
from zepben.ewb.model.cim.iec61968.customers.pricing_structure import PricingStructure
from zepben.ewb.model.cim.iec61968.customers.tariff import Tariff
from zepben.ewb.services.common.translator.base_cim2proto import document_to_pb, organisation_role_to_pb
from zepben.ewb.services.common.translator.util import mrid_or_empty
# noinspection PyProtectedMember
from zepben.ewb.services.customer.translator.customer_enum_mappers import _map_customer_kind


###################
# IEC61968 Common #
###################

def agreement_to_pb(cim: Agreement) -> PBAgreement:
    return PBAgreement(doc=document_to_pb(cim))


######################
# IEC61968 Customers #
######################

def customer_to_pb(cim: Customer) -> PBCustomer:
    customer = PBCustomer(
        kind=_map_customer_kind.to_pb(cim.kind),
        specialNeed=cim.special_need,
        customerAgreementMRIDs=[str(io.mrid) for io in cim.agreements]
    )

    getattr(customer, 'or').CopyFrom(organisation_role_to_pb(cim))
    return customer


def customer_agreement_to_pb(cim: CustomerAgreement) -> PBCustomerAgreement:
    return PBCustomerAgreement(
        agr=agreement_to_pb(cim),
        customerMRID=mrid_or_empty(cim.customer),
        pricingStructureMRIDs=[str(io.mrid) for io in cim.pricing_structures]
    )


def pricing_structure_to_pb(cim: PricingStructure) -> PBPricingStructure:
    return PBPricingStructure(
        doc=document_to_pb(cim),
        tariffMRIDs=[str(io.mrid) for io in cim.tariffs]
    )


def tariff_to_pb(cim: Tariff) -> PBTariff:
    return PBTariff(doc=document_to_pb(cim))


Agreement.to_pb = agreement_to_pb
Customer.to_pb = customer_to_pb
CustomerAgreement.to_pb = customer_agreement_to_pb
PricingStructure.to_pb = pricing_structure_to_pb
Tariff.to_pb = tariff_to_pb
