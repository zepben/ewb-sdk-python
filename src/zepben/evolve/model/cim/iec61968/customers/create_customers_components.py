#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from datetime import datetime
from typing import List

from zepben.evolve import *


def create_customer(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, organisation: Organisation = None, 
                    kind: CustomerKind = CustomerKind.UNKNOWN, customer_agreements: List[CustomerAgreement] = None) -> Customer:
    """
    Customer(OrganisationRole(IdentifiedObject))
    IdentifiedObject: mrid, name, description, names
    OrganisationRole: organisation
    Customer: kind, customer_agreements
    """
    c = Customer(**locals())
    if customer_agreements:
        for ca in customer_agreements:
            ca.customer = c
    return c


def create_customer_agreement(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, title: str = "",
                              created_date_time: datetime = None, author_name: str = "", type: str = "", status: str = "", comment: str = "",
                              customer: Customer = None, pricing_structures: List[PricingStructure] = None) -> CustomerAgreement:
    """
    CustomerAgreement(Agreement(Document(IdentifiedObject)))
    IdentifiedObject: mrid, name, description, names
    Document: title, created_date_time, author_name, type, status, comment
    Agreement: 
    CustomerAgreement: customer, pricing_structures
    """
    ca = CustomerAgreement(**locals())
    if customer:
        customer.add_agreement(ca)
    return ca


def create_pricing_structure(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, title: str = "",
                             created_date_time: datetime = None, author_name: str = "", type: str = "", status: str = "", comment: str = "",
                             tariffs: List[Tariff] = None) -> PricingStructure:
    """
    PricingStructure(Document(IdentifiedObject))
    IdentifiedObject: mrid, name, description, names
    Document: title, created_date_time, author_name, type, status, comment
    PricingStructure: tariffs
    """
    return PricingStructure(**locals())


def create_tariff(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, title: str = "", created_date_time: datetime = None,
                  author_name: str = "", type: str = "", status: str = "", comment: str = "") -> Tariff:
    """
    Tariff(Document(IdentifiedObject))
    IdentifiedObject: mrid, name, description, names
    Document: title, created_date_time, author_name, type, status, comment
    Tariff:
    """
    return Tariff(**locals())
