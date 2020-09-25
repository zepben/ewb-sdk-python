"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""


from dataclasses import dataclass

from zepben.protobuf.cim.iec61968.common.Agreement_pb2 import Agreement as PBAgreement
from zepben.protobuf.cim.iec61968.customers.CustomerAgreement_pb2 import CustomerAgreement as PBCustomerAgreement
from zepben.protobuf.cim.iec61968.customers.CustomerKind_pb2 import CustomerKind as PBCustomerKind
from zepben.protobuf.cim.iec61968.customers.Customer_pb2 import Customer as PBCustomer
from zepben.protobuf.cim.iec61968.customers.PricingStructure_pb2 import PricingStructure as PBPricingStructure
from zepben.protobuf.cim.iec61968.customers.Tariff_pb2 import Tariff as PBTariff

from zepben.cimbend import Customer
from zepben.cimbend.common.base_proto2cim import *
from zepben.cimbend.customer.customers import CustomerService
from zepben.cimbend.cim.iec61968.common.document import Agreement
from zepben.cimbend.cim.iec61968.customers import CustomerAgreement
from zepben.cimbend.cim.iec61968.customers import CustomerKind
from zepben.cimbend.cim.iec61968.customers import PricingStructure
from zepben.cimbend.cim.iec61968.customers import Tariff

__all__ = ["set_agreement", "CustomerProtoToCim"]


def set_agreement(pb: PBAgreement, cim: Agreement, service: BaseService):
    set_document(pb.doc, cim, service)


@dataclass
class CustomerProtoToCim(BaseProtoToCim):
    service: CustomerService

    def add_customer(self, pb: PBCustomer):
        cim = Customer(pb.mrid())
        self.set_organisation_role(getattr(pb, 'or'), cim)
        cim.kind = CustomerKind[PBCustomerKind.Name(pb.kind)]
        for mrid in pb.customerAgreementMRIDs:
            cim.add_agreement(self._get(mrid, CustomerAgreement, cim))
        self.service.add(cim)

    def add_customeragreement(self, pb: PBCustomerAgreement):
        customer = self._get(pb.customerMRID, Customer, pb.name_and_mrid())
        cim = CustomerAgreement(customer, pb.mrid())
        set_agreement(pb.agr, cim, self.service)
        for mrid in pb.pricingStructureMRIDs:
            cim.add_pricing_structure(self._get(mrid, PricingStructure, cim))
        self.service.add(cim)

    def add_pricingstructure(self, pb: PBPricingStructure):
        cim = PricingStructure(pb.mrid())
        set_document(pb.doc, cim, self.service)
        for mrid in pb.tariffMRIDs:
            cim.add_tariff(self._get(mrid, Tariff, cim))
        self.service.add(cim)

    def add_tariff(self, pb: PBTariff):
        cim = Tariff(pb.mrid())
        set_document(pb.doc, cim, self.service)
        self.service.add(cim)
